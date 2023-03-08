import asyncio
import re
import sys
from logging import Logger
from multiprocessing import Process
from typing import Any

import httpx
from httpx import AsyncHTTPTransport, AsyncClient
from packaging.version import parse as parse_version
from termcolor import colored

SERVICES = {
    'nextcloud': '25.0.4',
    'gitea/gitea': '1.18.5',
    'caddy': '2.6.4',
    'mediawiki': '1.39.2',
    'bitwarden/server': '2023.2.0',
    'redis': '7.0.8',
    'nginx': '1.23.3',
    'mariadb': '10.11.2',
    'postgres': '15.2',
    'mysql': '8.0.32',
    'selenoid/firefox': '110.0',
    'python': '3.11.1',
}


def configure_logger() -> Logger:
    try:
        from loguru import logger as loguru_logger

        loguru_logger.remove()
        loguru_logger.add(
            sink=sys.stdout,
            colorize=True,
            level='DEBUG',
            format='<cyan>{time:DD.MM.YYYY HH:mm:ss}</cyan> | <level>{level}</level> | <magenta>{message}</magenta>',
        )
        return loguru_logger  # type: ignore
    except ImportError:
        import logging

        logging_logger = logging.getLogger('main_logger')
        formatter = logging.Formatter(
            datefmt='%Y.%m.%d %H:%M:%S',
            fmt='%(asctime)s | %(levelname)s | func name: %(funcName)s | message: %(message)s',
        )
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(formatter)
        logging_logger.setLevel(logging.INFO)
        logging_logger.addHandler(handler)
        return logging_logger


logger = configure_logger()


class DockerHubScanner:

    # bitwarden/server
    # https://hub.docker.com/v2/namespaces/bitwarden/repositories/server/tags?page=2

    # caddy
    # https://registry.hub.docker.com/v2/repositories/library/caddy/tags?page=1

    DOCKERHUB_REGISTRY_API = 'https://registry.hub.docker.com/v2/repositories/library'
    DOCKERHUB_API = 'https://hub.docker.com/v2/namespaces'

    def _docker_hub_api_url(self, service_name: str) -> str:

        if '/' in service_name:
            namespace, name = service_name.split('/')
            url = f'{self.DOCKERHUB_API}/{namespace}/repositories/{name}/tags'
        else:
            url = f'{self.DOCKERHUB_REGISTRY_API}/{service_name}/tags'
        return url

    @staticmethod
    async def _async_request(client: AsyncClient, url: str) -> dict[str, Any] | None:

        response = await client.get(url)
        status = response.status_code
        if status == httpx.codes.OK:
            return response.json()
        return None

    @staticmethod
    def _get_next_page_and_tags_from_payload(payload: dict[str, Any]) -> tuple[str | None, list[str]]:
        next_page = payload['next']
        names = [release['name'] for release in payload['results']]
        return next_page, names

    async def get_tags(self, service_name: str) -> dict[str, list[str]]:
        """
        To make method really async it should be rewritten on pages not by get next page each time.
        Also, dockerhub protected from bruteforce requests.
        Better with getting next page each time
        """

        tags = []
        url = self._docker_hub_api_url(service_name)
        transport = AsyncHTTPTransport(retries=1)
        async with AsyncClient(transport=transport) as client:
            payload = await self._async_request(client=client, url=url)

            if not payload:
                return {service_name: tags}

            next_page, names = self._get_next_page_and_tags_from_payload(payload)

            tags.extend(names)

            while SERVICES[service_name] not in tags:
                payload = await self._async_request(client=client, url=next_page)
                next_page, names = self._get_next_page_and_tags_from_payload(payload)
                tags.extend(names)

            # filter tags contains versions 1.18.3 and not contains letters 1.18.3-fpm-alpine. Sort by version number
            tags = sorted(
                list(filter(lambda t: re.search(r'\d+\.\d', t) and not re.search(r'[a-z]', t), tags)),
                reverse=True,
                key=parse_version,
            )

            # Do not show older versions than current in tags
            tags = tags[:tags.index(SERVICES[service_name]) + 1]
        return {service_name: tags}

    def get_data(self, service_name: str) -> dict[str, list[str]]:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        services_tags = loop.run_until_complete(self.get_tags(service_name))

        return services_tags

    def print_data(self, service_name: str) -> None:

        data = self.get_data(service_name)
        print(
            f"Service: {colored(service_name, color='light_grey')}",
            f"\nTags: {colored(str(data[service_name]), color='magenta')}",
            f"\nCurrent version: {colored(SERVICES[service_name], color='cyan')}"
        )

        if data[service_name][0] > SERVICES[service_name]:
            print(f"New version of {service_name}: {colored(data[service_name][0], color='yellow')}")
        print()


if __name__ == '__main__':

    print('Services'.center(50, '-'), '\n')

    dockerhub_scanner = DockerHubScanner()
    processes = []

    for service in SERVICES:
        process = Process(target=dockerhub_scanner.print_data, kwargs={'service_name': service})
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

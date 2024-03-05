import asyncio
import re
import sys
from logging import Logger
from multiprocessing import Process, Lock
from typing import Any

import httpx
from httpx import AsyncHTTPTransport, AsyncClient
from packaging.version import parse as parse_version
from termcolor import colored

SERVICES: dict[str: dict[str, Any]] = {
    'general': {
        'components': [
            {'name': 'caddy', 'version': '2.7.6'},
            {'name': 'python', 'version': '3.12.2'},
        ]
    },
    'nextcloud': {
        'components': [
            {'name': 'nextcloud', 'version': '28.0.3'},
            {'name': 'mysql', 'version': '8.3.0'},
            {'name': 'redis', 'version': '7.2.4'},
            {'name': 'nginx', 'version': '1.25.4'},
            {'name': 'onlyoffice/documentserver', 'version': '8.0.1.1'},
        ],
    },
    'gitea': {
        'components': [
            {'name': 'gitea/gitea', 'version': '1.21.7'},
            {'name': 'postgres', 'version': '16.2'},
        ],
    },
    'mediawiki': {
        'components': [
            {'name': 'mediawiki', 'version': '1.41.0'},
            {'name': 'mariadb', 'version': '11.3.2'},
        ],
    },
    'bitwarden': {
        'components': [
            {'name': 'bitwarden/web', 'version': '2024.2.2'},
            {'name': 'bitwarden/server', 'version': '2024.2.2'},
        ],
    },
    'mosgortrans': {
        'deprecated': False,
        'components': [
            {'name': 'selenoid/chrome', 'version': '121.0'},
            {'name': 'aerokube/selenoid', 'version': '1.11.2'},
        ],
    },
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
    """Url server examples:
    bitwarden/server
    https://hub.docker.com/v2/namespaces/bitwarden/repositories/server/tags?page=2

    caddy
    https://registry.hub.docker.com/v2/repositories/library/caddy/tags?page=1
    """

    DOCKERHUB_REGISTRY_API = 'https://registry.hub.docker.com/v2/repositories/library'
    DOCKERHUB_API = 'https://hub.docker.com/v2/namespaces'

    async def get_tags(self, service_name: str, service_component: dict[str, str]) -> dict[str, list[str]]:
        """
        To make method really async it should be rewritten on pages not by get next page each time.
        Also, dockerhub protected from bruteforce requests.
        Better with getting next page each time
        """
        component_name = service_component['name']
        component_version = service_component['version']

        url = self._docker_hub_api_url(component_name)
        all_tags = []
        transport = AsyncHTTPTransport(retries=1)
        async with AsyncClient(transport=transport) as client:
            payload = await self._async_request(client=client, url=url)

            if not payload:
                return {component_name: all_tags}

            next_page, tags = self._get_next_page_and_tags_from_payload(payload)

            all_tags.extend(tags)

            while component_version not in all_tags:
                if not next_page:
                    break
                payload = await self._async_request(client=client, url=next_page)
                next_page, tags = self._get_next_page_and_tags_from_payload(payload)
                all_tags.extend(tags)

            # filter tags contains versions 1.18.3 and not contains letters 1.18.3-fpm-alpine. Sort by version number
            tags = sorted(
                list(
                    filter(
                        lambda t: re.search(r'\d+\.\d', t) and not re.search(r'[a-z]', t),
                        all_tags,
                    )
                ),
                reverse=True,
                key=parse_version,
            )

            # Do not show older versions than current in tags
            try:
                tags = tags[:tags.index(component_version) + 1]
                if len(tags) > 5:
                    tags = tags[:5]
            except ValueError:
                tags = tags[:3]
                logger.error(
                    f"Cant find tag {component_version} for service {service_name} for component {component_name}"
                )
        return {component_name: tags}

    def get_data(self, service_name: str, service_component: dict[str, str]) -> dict[str, list[str]]:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        services_tags = loop.run_until_complete(self.get_tags(service_name, service_component))

        return services_tags

    def print_data(self, service_name: str, service_component: dict[str, str]) -> None:

        component_name = service_component['name']
        component_version = service_component['version']

        data = self.get_data(service_name, service_component)

        print(
            f"Service: {colored(service_name, color='light_grey')}",
            f"\nComponent: {colored(component_name, color='light_blue')}",
            f"\nLatest tags: {colored(str(data[component_name]), color='magenta')}",
            f"\nCurrent version: {colored(component_version, color='cyan')}",
        )

        if data[component_name][0] > component_version:
            print(f"New version of {component_name}: {colored(data[component_name][0], color='yellow')}")
        print()

    async def _async_request(self, client: AsyncClient, url: str) -> dict[str, Any] | None:

        response = await client.get(url)
        status = response.status_code
        if status == httpx.codes.OK:
            return response.json()
        else:
            uri = url.replace(self.DOCKERHUB_REGISTRY_API, '').replace(self.DOCKERHUB_API, '')
            logger.info(f'got response status: {status} for uri: {uri}')
        return None

    def _docker_hub_api_url(self, service_name: str) -> str:

        if '/' in service_name:
            namespace, name = service_name.split('/')
            url = f'{self.DOCKERHUB_API}/{namespace}/repositories/{name}/tags'
        else:
            url = f'{self.DOCKERHUB_REGISTRY_API}/{service_name}/tags'
        return url

    @staticmethod
    def _get_next_page_and_tags_from_payload(payload: dict[str, Any]) -> tuple[str | None, list[str]]:
        next_page = payload['next']
        names = [release['name'] for release in payload['results']]
        return next_page, names


if __name__ == '__main__':

    print()
    print(colored('Services'.center(50, '-', ), color='white'), '\n')

    lock = Lock()

    dockerhub_scanner = DockerHubScanner()
    processes = []

    with lock:
        for service, service_details in SERVICES.items():
            for component in service_details['components']:
                if service_details.get('deprecated', False):
                    continue
                process = Process(
                    target=dockerhub_scanner.print_data,
                    kwargs={'service_name': service, 'service_component': component}
                )
                processes.append(process)
                process.start()

            for process in processes:
                process.join()

    print(colored("All jobs done", color='white'), '\n')


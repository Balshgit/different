import asyncio
import time
from socket import gaierror
from typing import List, Tuple, Union, Dict, Optional
import aiohttp
from aiohttp.client_exceptions import TooManyRedirects
import logging
import sys
from collections import Counter
from functools import wraps

HEADERS = {
    'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0 ', }

console_logger = logging.getLogger(__name__)
formatter = logging.Formatter(datefmt="%Y.%m.%d %H:%M:%S",
                              fmt='%(asctime)s | message: %(message)s')
                              # fmt='%(asctime)s | %(levelname)s | process: %(process)d | module name: %(name)s | '
                              #     'func name: %(funcName)s | line number: %(lineno)s | message: %(message)s',)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(formatter)
console_logger.setLevel(logging.INFO)
console_logger.addHandler(handler)


def time_to_execute(time_form='sec'):
    """
    select time format:
    'sec': in seconds
    'min': in minutes
    'hour': in hours
    """

    multiply = {'sec': 1, 'min': 60, 'hour': 3600}

    def wrapper(func):
        @wraps(func)
        def new_func(*args, **kwargs):
            begin = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            exec_time = (end - begin) / multiply[time_form]
            console_logger.info(f'Duration {func.__name__}, {time_form}: {exec_time}')
            return result

        return new_func

    return wrapper


class NetScanner:
    """
    Scan urls asyncable
    :param logger: Setup logger | logging.Logger
    """

    def __init__(self, sem: int, logger: logging.Logger) -> None:
        self.logger = logger
        self.sem = asyncio.Semaphore(sem)
        self.count = 0

    async def _head_request(self, session: aiohttp.ClientSession, url: str, timeout: int) -> Union[str, None]:
        """
        Get ip address and send HEAD request to it. If HEAD request is unavailable send GET request
        :param session: Http session for request | aiohttp.ClientSession
        :param ip: Get ip which server will be checked | str
        :param timeout: set timeout to wait in seconds | int
        :return: Ip with status OK | str
        """
        try:
            # A HEAD request is quicker than a GET request
            async with self.sem:
                self.count += 1
                console_logger.info(f'Count of total requests: {self.count}')
                resp = await session.head(url, allow_redirects=True, ssl=False, timeout=timeout)
                async with resp:
                    status = resp.status
                    if status and status == 200:
                        return url
                    if status == 405:
                        # HEAD request not allowed, fall back on GET
                        resp = await session.get(url, allow_redirects=True, ssl=False, timeout=timeout)
                        async with resp:
                            status = resp.status
                            if status and status == 200:
                                return url
        except aiohttp.InvalidURL as e:
            self.logger.error(f"Invalid url: {str(e)}")
        except aiohttp.ClientConnectorError as e:
            self.logger.error(f"Unreachable: {str(e)}")
        except gaierror as e:
            self.logger.error(f"Gaierror: {str(e)}")
        except aiohttp.ServerDisconnectedError as e:
            self.logger.error(f"Disconnected error: {str(e)}")
        except aiohttp.ClientOSError as e:
            self.logger.error(f"ClientOS error: {str(e)}")
        except TooManyRedirects as e:
            self.logger.error(f"To many redirects: {str(e)}")
        except aiohttp.ClientResponseError as e:
            self.logger.error(f"Client response error: {str(e)}")
        except aiohttp.ServerTimeoutError as e:
            self.logger.error(f"Server timeout error: {str(e)}")
        except asyncio.TimeoutError as e:
            self.logger.error(f"Connection timeout:{str(e)}")

    async def _get_servers_by_response(self, ip_addresses: List[str], timeout: int) -> List[str]:
        """
        Get list of ip addresses and return which of them is available
        :param ip_addresses: list of ip addresses | List[str]
        :param timeout: set timeout to wait in seconds | int
        :return: List of ip addresses | List[str]
        """
        # Next setting is configure dns and limit of connections for session like
        # aiohttp.ClientSession(connector=connector, shared_timeout=timeout)
        connector = aiohttp.TCPConnector(limit=500)
        # shared_timeout = aiohttp.ClientTimeout(total=5)

        async with aiohttp.ClientSession(connector=connector) as session:
            servers = await asyncio.gather(*[self._head_request(session, ip, timeout) for ip in ip_addresses])
            return list(servers)

    def ping_servers(self, ip_addresses: List[str], timeout) -> Tuple[str]:
        """
        Loops through the ip addresses, head request each, append available to potential servers tuple
        :param ip_addresses: bunch of ip addresses | list []
        :param timeout: set timeout to wait in seconds | int
        :return: available servers | tuple()
        """
        self.logger.info("Started polling potential servers")
        time1 = time.time()
        loop = asyncio.get_event_loop()
        servers = loop.run_until_complete(self._get_servers_by_response(ip_addresses, timeout))
        time2 = time.time()
        dt = time2 - time1
        self.logger.info(f"Polled potential servers {len(servers)} servers in {dt:.1f} seconds "
                         f"at {len(servers) / dt:.3f} Servers/sec")
        return tuple(servers)


server_checker = NetScanner(200, console_logger)
urls = ['https://httpbin.org/delay/10' for _ in range(3000)]
available_urls = server_checker.ping_servers(urls, timeout=15)
console_logger.info(f'Ping result: {Counter(available_urls).most_common(2)}')

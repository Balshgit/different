import asyncio
import sys
import time
from logging import Logger
from multiprocessing import Process
from typing import Any

import aiohttp
import requests


def configure_logger() -> Logger:
    try:
        from loguru import logger as loguru_logger

        loguru_logger.remove()
        loguru_logger.add(
            sink=sys.stdout,
            colorize=True,
            level='DEBUG',
            format="<cyan>{time:DD.MM.YYYY HH:mm:ss}</cyan> | <level>{level}</level> | <magenta>{message}</magenta>",
        )
        return loguru_logger  # type: ignore
    except ImportError:
        import logging

        logging_logger = logging.getLogger('main_logger')
        formatter = logging.Formatter(
            datefmt="%Y.%m.%d %H:%M:%S",
            fmt='%(asctime)s | %(levelname)s | func name: %(funcName)s | message: %(message)s',
        )
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(formatter)
        logging_logger.setLevel(logging.INFO)
        logging_logger.addHandler(handler)
        return logging_logger


logger = configure_logger()


class GoodGame:
    BASE_URL = 'https://goodgame.ru/api/4/streams'
    PAGES_FOR_ASYNC_SCAN = 25
    CURRENT_WATCHERS_FILTER = 1

    def __init__(self) -> None:
        self.all_streams: dict[int, dict[str, Any]] = dict()

    @staticmethod
    def _show_time_and_result(message: str) -> Any:
        def wrapper(func: Any) -> Any:
            def new_func(*args: Any, **kwargs: Any) -> None:
                begin = time.time()
                result = func(*args, **kwargs)
                end = time.time()
                logger.info(f'{message} execution time, sec: {round(end - begin, 2)}')
                print(result)

            return new_func

        return wrapper

    def get_last_page_number(self) -> int:
        """
        Deprecated
        """
        last_page = 1
        for page in range(20, 0, -1):
            response = requests.get(f'{self.BASE_URL}?page={page}')
            if response.json()["streams"]:
                last_page = page
                break
        return last_page

    def get_max_current_viewers_count(self) -> int | None:
        """
        Deprecated
        """
        response = requests.get(f'{self.BASE_URL}?page=1')
        max_current_viewers = response.json()['streams'][0].get('viewers', None)
        return max_current_viewers

    def _sort_trim_dict(self, data: dict[str, int]) -> dict[str, int]:
        sorted_data = dict(sorted(data.items(), key=lambda x: x[1], reverse=True))
        new_data = {
            stream: viewers_count
            for stream, viewers_count in sorted_data.items()
            if int(viewers_count) >= self.CURRENT_WATCHERS_FILTER
        }
        return new_data

    def __count_streams_with_watchers(self, current_watchers: list[int]) -> int:
        return len(
            list(
                filter(
                    lambda stream: stream['viewers'] in current_watchers,
                    self.all_streams.values(),
                )
            )
        )

    def __prepare_result(self, max_current_viewers: int) -> str:
        total_viewers: dict[str, int] = dict()
        for stream in self.all_streams.values():
            if (
                max_current_viewers
                and int(stream.get('viewers', 0)) <= max_current_viewers
            ):
                total_viewers[
                    f'{stream["streamer"]["username"]} [{stream["game"]["url"]}]'
                ] = int(stream['viewers'])
        watchers_0 = self.__count_streams_with_watchers(current_watchers=[0])
        watchers_1 = self.__count_streams_with_watchers(current_watchers=[1])
        minimal_watchers = self.__count_streams_with_watchers(current_watchers=[0, 1])
        return (
            f'Total streams: {len(self.all_streams)} -> '
            f'with minimal watchers {round(minimal_watchers / len(self.all_streams) * 100)}%\n'
            f'Total streams with 0 viewers: {watchers_0} -> {round(watchers_0/len(self.all_streams) * 100)}%\n'
            f'Total streams with 1 viewer: {watchers_1} -> {round(watchers_1/len(self.all_streams) * 100)}%\n'
            f'Total viewers: {sum(total_viewers.values())}\n'
            f'Streams: {self._sort_trim_dict(total_viewers)}\n'
            f'{"-"*76}'
        )

    async def _async_request(self, session: aiohttp.ClientSession, url: str) -> None:
        async with asyncio.Semaphore(500):
            counter = 0
            while True:
                try:
                    counter += 1
                    resp = await session.get(url)
                    async with resp:
                        if resp.status == 200:
                            data = await resp.json()
                            for stream in data['streams']:
                                self.all_streams.update({stream['id']: stream})
                            return data['streams']
                except Exception as connection_error:
                    if counter < 5:
                        await asyncio.sleep(10)
                    else:
                        raise connection_error

    async def _async_data_scrapper(self) -> int:
        async with aiohttp.ClientSession() as session:

            streams = await asyncio.gather(
                *[
                    self._async_request(session, f'{self.BASE_URL}?page={page}')
                    for page in range(1, self.PAGES_FOR_ASYNC_SCAN + 1)
                ],
                return_exceptions=True,
            )
        max_current_viewers = streams[0][0]['viewers']
        return max_current_viewers

    @_show_time_and_result(message='Async counter')
    def async_counter(self) -> str:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        max_current_viewers = loop.run_until_complete(self._async_data_scrapper())
        return self.__prepare_result(max_current_viewers)

    @_show_time_and_result(message='Sync counter')
    def sync_counter(self) -> str:
        page = 1

        response = requests.get(f'{self.BASE_URL}?page={page}', timeout=2)
        streams = response.json()['streams']
        for stream in streams:
            self.all_streams.update({stream['id']: stream})
        max_current_viewers = streams[0]['viewers']
        while streams:
            page += 1
            response = requests.get(f'{self.BASE_URL}?page={page}')
            streams = response.json()['streams']
            for stream in streams:
                self.all_streams.update({stream['id']: stream})
        return self.__prepare_result(max_current_viewers)


if __name__ == '__main__':
    print("-" * 76)
    good_game = GoodGame()
    start = time.time()
    good_game.async_counter()
    # async_process = Process(
    #     target=good_game.async_counter, args=(), kwargs={}, name='async_process'
    # )
    # sync_process = Process(
    #     target=good_game.sync_counter, args=(), kwargs={}, name='sync_process'
    # )

    # sync_process.start()
    # async_process.start()
    # sync_process.join()
    # async_process.join()

    stop = time.time()
    logger.info(f'End all processes. Execution time: {round(stop-start, 2)} seconds')

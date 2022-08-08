import os
import sys
import tarfile
import time
from dataclasses import dataclass
from pathlib import Path

import wget
from loguru import logger
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox import options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.webdriver import WebDriver

from aiogram import Bot, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.webhook import SendMessage
from aiogram.utils.executor import start_webhook

logger.remove()
logger.add(sink=sys.stdout, colorize=True, level='DEBUG',
           format="<cyan>{time:DD.MM.YYYY HH:mm:ss}</cyan> | <level>{level}</level> | "
                  "<magenta>{message}</magenta>")


GECKO_DRIVER_VERSION = '0.31.0'
BASE_DIR = Path(__file__).parent.resolve().as_posix()

API_TOKEN = os.environ.get('API_TOKEN')

# webhook settings
WEBHOOK_HOST = 'https://bot.mywistr.com'
WEBHOOK_PATH = '/transport'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# webserver settings
WEBAPP_HOST = 'test-server.lan'  # or ip
WEBAPP_PORT = 8084


bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


@dataclass
class Description:
    id: int
    description: str


def download_gecko_driver():
    gecko_driver = f'https://github.com/mozilla/geckodriver/releases/download/v{GECKO_DRIVER_VERSION}/' \
                   f'geckodriver-v{GECKO_DRIVER_VERSION}-linux64.tar.gz'

    if not Path(f'{BASE_DIR}/geckodriver').exists():
        logger.info(f'Downloading gecodriver v {GECKO_DRIVER_VERSION}...')
        geckodriver_file = wget.download(url=gecko_driver, out=BASE_DIR)

        with tarfile.open(geckodriver_file) as tar:
            tar.extractall(BASE_DIR)
        os.remove(f'{BASE_DIR}/geckodriver-v{GECKO_DRIVER_VERSION}-linux64.tar.gz')
        logger.info(f'\ngeckodriver has been downloaded to folder {BASE_DIR}')


def configure_firefox_driver(private_window: bool = False) -> WebDriver:
    opt = options.Options()
    opt.headless = True
    opt.add_argument('-profile')
    opt.add_argument(f'{Path.home()}/snap/firefox/common/.mozilla/firefox')
    if private_window:
        opt.set_preference("browser.privatebrowsing.autostart", True)
    service = Service(executable_path=f'{BASE_DIR}/geckodriver')
    firefox_driver = webdriver.Firefox(service=service, options=opt)

    return firefox_driver


def parse_site() -> str:
    driver.get(
        'https://yandex.ru/maps/213/moscow/stops/stop__9640740/?l=masstransit&ll=37.527754%2C55.823507&tab=overview&z=21'
    )
    time.sleep(4)
    elements = driver.find_elements(by='class name', value='masstransit-vehicle-snippet-view')

    bus_300, bus_t19 = None, None
    bus_300_arrival, bus_t19_arrival = None, None

    for element in elements:
        try:
            bus_300 = element.find_element(by='css selector', value='[aria-label="300"]')
            bus_300_arrival = element.find_element(by='class name', value='masstransit-prognoses-view__title-text')
        except NoSuchElementException:
            pass
        try:
            bus_t19 = element.find_element(by='css selector', value='[aria-label="т19"]')
            bus_t19_arrival = element.find_element(by='class name', value='masstransit-prognoses-view__title-text')
        except NoSuchElementException:
            pass
    return f'{bus_300.text} - {bus_300_arrival.text}\n{bus_t19.text} - {bus_t19_arrival.text}'


@dp.message_handler()
async def echo(message: types.Message):
    # Regular request
    # await bot.send_message(message.chat.id, message.text)

    text = parse_site()

    # or reply INTO webhook
    return SendMessage(message.chat.id, text)


async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)
    # insert code here to run it after start


async def on_shutdown(dp):
    logger.warning('Shutting down..')

    # insert code here to run it before shutdown

    # Remove webhook (not acceptable in some cases)
    await bot.delete_webhook()

    # Close DB connection (if used)
    await dp.storage.close()
    await dp.storage.wait_closed()

    logger.warning('Bye!')


if __name__ == '__main__':
    download_gecko_driver()
    driver = configure_firefox_driver()
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )


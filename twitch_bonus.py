import argparse
import atexit
import os
import sys
import tarfile
import time
from pathlib import Path
from typing import Optional

import validators
import wget
from loguru import logger
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox import options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.webdriver import WebDriver
from urllib3.exceptions import MaxRetryError

logger.remove()
logger.add(sink=sys.stdout, colorize=True, level='DEBUG',
           format="<cyan>{time:DD.MM.YYYY HH:mm:ss}</cyan> | <level>{level}</level> | "
                  "<magenta>{message}</magenta>")


GECKO_DRIVER_VERSION = '0.31.0'
BASE_DIR = Path(__file__).parent.resolve().as_posix()

TWITCH_USERNAME = os.environ.get('TWITCH_USERNAME')
TWITCH_PASSWORD = os.environ.get('TWITCH_PASSWORD')
if not all([TWITCH_USERNAME, TWITCH_PASSWORD]):
    raise Exception('Username and password must be set')


def download_gecko_driver():
    logger.info(f'Downloading gecodriver v {GECKO_DRIVER_VERSION}...')

    gecko_driver = f'https://github.com/mozilla/geckodriver/releases/download/v{GECKO_DRIVER_VERSION}/' \
                   f'geckodriver-v{GECKO_DRIVER_VERSION}-linux64.tar.gz'

    geckodriver_file = wget.download(url=gecko_driver, out=BASE_DIR)

    with tarfile.open(geckodriver_file) as tar:
        tar.extractall(BASE_DIR)
    os.remove(f'{BASE_DIR}/geckodriver-v{GECKO_DRIVER_VERSION}-linux64.tar.gz')
    print(f'\ngeckodriver has been downloaded to folder {BASE_DIR}')


def configure_firefox_driver(private_window: bool = False) -> WebDriver:
    opt = options.Options()
    opt.headless = False
    opt.add_argument('-profile')
    opt.add_argument(f'{Path.home()}/snap/firefox/common/.mozilla/firefox')
    if private_window:
        opt.set_preference("browser.privatebrowsing.autostart", True)
    service = Service(executable_path=f'{BASE_DIR}/geckodriver')
    firefox_driver = webdriver.Firefox(service=service, options=opt)

    return firefox_driver


def validate_stream_url(twitch_url: str) -> Optional[str]:

    twitch_url_valid = validators.url(twitch_url)
    if twitch_url_valid is not True:
        logger.error(f'Url {twitch_url} is invalid. Please provide correct one.')
        sys.exit(1)
    return twitch_url


class UserExitException(Exception):
    """We use this exception when user wants to exit."""


def exit_log(message: str):
    try:
        logger.info(message)
        driver.close()
        os.remove(f'{os.getcwd()}/geckodriver.log')
        sys.exit(0)
    except MaxRetryError:

        pass
    except SystemExit:
        os.abort()


def main(twitch_url: str):
    try:
        try:
            driver.get(twitch_url)
            time.sleep(4)
            try:
                elem = driver.find_element(by='css selector', value='[data-a-target="login-button"]')
                elem.click()
                logger.info('you have 60 seconds to login')
                time.sleep(2)
                login = driver.find_element(by='css selector', value='[aria-label="Enter your username"]')
                login.clear()
                login.send_keys(f'{TWITCH_USERNAME}')
                password = driver.find_element(by='css selector', value='[aria-label="Enter your password"]')
                password.clear()
                password.send_keys(f'{TWITCH_PASSWORD}')
                time.sleep(1)
                password.send_keys(Keys.ENTER)
                time.sleep(53)
                logger.info('time for login is up')
            except NoSuchElementException:
                logger.info('Login button not found. Probably you are already logged in')
            try:
                security_button = driver.find_element(
                    by='css selector',
                    value='[data-a-target="account-checkup-generic-modal-secondary-button"]'
                )
                security_button.click()
            except NoSuchElementException:
                logger.info('Security button not found, continue...')
        except Exception as e:
            logger.error(f'Open page exception: {e}')

        total_bonus, clicks = 0, 0
        while True:
            try:
                elem = driver.find_element(by='css selector', value='[aria-label="Claim Bonus"]')
                elem.click()
                total_bonus += 50
                clicks += 1
                logger.info(f'{clicks}-bonus +50 has been clicked! Total bonus: {total_bonus}')
                time.sleep(60 * 15 - 2)
            except NoSuchElementException:
                time.sleep(1)
            except ElementClickInterceptedException:
                logger.error('Security button must be clicked')
                time.sleep(15 * 60)
            except UserExitException:
                break

    except KeyboardInterrupt as e:
        atexit.register(exit_log, 'Exit script')


if __name__ == '__main__':

    parser = argparse.ArgumentParser('Twitch clicker', add_help=True)
    parser.add_argument('-u', '--twitch_url', required=False, default='https://www.twitch.tv/lol4to22',
                        help='Please provide twitch stream url')

    args = parser.parse_args(sys.argv[1:])

    url = 'https://www.twitch.tv/lol4to22'

    stream_url = args.twitch_url
    if stream_url:
        url = validate_stream_url(stream_url)
    logger.info(f'Stream url is: {url}')

    download_gecko_driver()
    driver = configure_firefox_driver()

    main(url)

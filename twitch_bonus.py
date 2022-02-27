import atexit
import os
import sys
import time

from loguru import logger
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox import options
from selenium.webdriver.firefox.service import Service
from urllib3.exceptions import MaxRetryError

logger.remove()
logger.add(sink=sys.stdout, colorize=True, level='DEBUG',
           format="<cyan>{time:DD.MM.YYYY HH:mm:ss}</cyan> | <level>{level}</level> | "
                  "<magenta>{message}</magenta>")

opt = options.Options()
opt.headless = False
service = Service(executable_path=r'./geckodriver')
driver = webdriver.Firefox(service=service, options=opt)


class UserExitException(Exception):
    """We use this exception when user wants to exit."""


def exit_log(message: str):
    try:
        logger.info(message)
        driver.close()
        sys.exit(0)
    except MaxRetryError:
        pass
    except SystemExit:
        os.abort()


if __name__ == '__main__':
    try:
        try:
            driver.get("https://www.twitch.tv/lol4to22")
            logger.info('you have 60 seconds to login')
            time.sleep(60)
            logger.info('time for login is up')
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
            except UserExitException:
                break
    except KeyboardInterrupt as e:
        atexit.register(exit_log, 'Exit script')

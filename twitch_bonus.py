import sys
import time
import atexit

from loguru import logger
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox import options
from urllib3.exceptions import MaxRetryError

logger.remove()
logger.add(sink=sys.stdout, colorize=True, level='DEBUG',
           format="<cyan>{time:YYYY.MM.DD HH:mm:ss}</cyan> | <level>{level}</level> | "
                  "<magenta>{message}</magenta>")

opt = options.Options()
opt.headless = False
service = Service(executable_path=r'./geckodriver')
driver = webdriver.Firefox(service=service, options=opt)


def exit_log(message: str):
    logger.info(message)
    try:
        driver.close()
    except MaxRetryError:
        pass


if __name__ == '__main__':
    try:
        try:
            driver.get("https://www.twitch.tv/lol4to22")

            logger.info('you have 60 seconds to login')
            time.sleep(60)
            logger.info('time for login is up')
        except Exception as e:
            logger.error(f'Open page exception: {e}')

        while True:
            try:
                elem = driver.find_element(by='css selector', value='[aria-label="Claim Bonus"]')
                elem.click()
                logger.info('Bonus +50 has been clicked!')
            except Exception as e:
                pass
            time.sleep(15)
    except KeyboardInterrupt as e:
        atexit.register(exit_log, 'Exit script')

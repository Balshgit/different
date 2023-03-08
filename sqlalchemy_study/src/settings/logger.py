import logging
import sys

from loguru import logger

logger.remove()

formatter = "<cyan>{time}</cyan> | <level>{level}</level> | <magenta>{message}</magenta>"
sink = sys.stdout

logger.add(sink=sink, colorize=True, level=logging.INFO, format=formatter)

import importlib.util
import logging
import sys

from decouple import AutoConfig
from pathlib import Path

current_dir = Path(__file__).parent.parent
config = AutoConfig(search_path=current_dir.joinpath('get_project_core'))


# use loguru if it is possible for color output
if importlib.util.find_spec('loguru') is not None:
    from loguru import logger
    logger.remove()
    logger.add(sink=sys.stdout, colorize=True, level='DEBUG',
               format="<cyan>{time:DD.MM.YYYY HH:mm:ss}</cyan> | <level>{level}</level> | "
                      "<magenta>{message}</magenta>")

# use standard logging
else:
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    log_formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    console_handler.setFormatter(log_formatter)

    logger.addHandler(console_handler)

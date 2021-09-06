from celery import Celery
from celery.signals import after_setup_logger
from celery.utils.log import get_task_logger
# from server.settings.components import config
from pathlib import Path, PurePath
from decouple import AutoConfig
import logging


logger = logging.getLogger('My_logger')

# @after_setup_logger.connect
def conf_celery_logger(logger, **kwargs):
    formatter = logging.Formatter(datefmt="%Y.%m.%d %H:%M:%S",
                                  fmt='%(asctime)s | %(levelname)s | '
                                      'process: %(process)d | '
                                      'module name: %(name)s | '
                                      'func name: %(funcName)s | '
                                      'line number: %(lineno)s | '
                                      'message: %(message)s',)
    handler = logging.FileHandler('log.log')
    handler.setLevel('DEBUG')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel('DEBUG')


conf_celery_logger(logger)

# BASE_DIR = Path.cwd().parent.parent
BASE_DIR = PurePath(__file__).parent

config = AutoConfig(search_path=BASE_DIR.joinpath('config'))

RABBITMQ_DEFAULT_USER = config('RABBITMQ_DEFAULT_USER')
RABBITMQ_DEFAULT_PASS = config('RABBITMQ_DEFAULT_PASS')
RABBITMQ_PORT = config('RABBITMQ_PORT', cast=int, default=5672)
RABBITMQ_HOST = config('RABBITMQ_HOST')


celery_app = Celery(
    'tasks',
    broker='amqp://{login}:{password}@{host}:{port}'.format(
        login=RABBITMQ_DEFAULT_USER,
        password=RABBITMQ_DEFAULT_PASS,
        host=RABBITMQ_HOST,
        port=RABBITMQ_PORT,
    ),
    backend='rpc://',
)

celery_app.config_from_object('config.celeryconfig')
# celery_app.conf.update({'worker_hijack_root_logger': False})

celery_app.autodiscover_tasks()

logger.info(f"{__name__} imported {celery_app.conf['worker_hijack_root_logger']}")

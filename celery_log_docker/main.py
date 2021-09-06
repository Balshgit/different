import logging

from celery_config import celery_app as app
from celery.utils.log import get_task_logger


#logger = get_task_logger('My_logger')

logger = logging.getLogger('My_logger')

# logger.addHandler(handler)
# logger.setLevel('DEBUG')


@app.task()
def test(x: int, y: int) -> int:
    logger.info('WE ARE HERE')
    print(x + y)
    result = x + y
    logger.info(result)
    return result


# test(6, 8)
logger.info(f'{__name__} imported')

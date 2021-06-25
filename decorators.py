import datetime
from functools import wraps
from datetime import datetime


def func_exec_count(func):
    @wraps(func)
    def new_func(*args, **kwargs):
        func_result = func(*args, **kwargs)
        new_func.count += 1
        return func_result
    new_func.count = 0
    return new_func


def execution_time(func):
    @wraps(func)
    def exec_func(*args, **kwargs):
        now = datetime.now()
        func_result = func(*args, **kwargs)
        end = datetime.now()
        print('time to execute', (end - now).seconds)
        return func_result
    return exec_func


@func_exec_count
@execution_time
def summary(x: int, y: int) -> int:
    z = x + y
    return z


@execution_time
def main():
    result = 0
    for i in range(1, 11):
        result += summary(i, 100)
        print(result)
    print(summary.count, summary.__name__)


main()

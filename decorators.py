from functools import wraps
import time


def func_exec_count(func):
    @wraps(func)
    def new_func(*args, **kwargs):
        func_result = func(*args, **kwargs)
        new_func.count += 1
        return func_result
    new_func.count = 0
    return new_func


def execution_time(time_form='sec'):
    multiply = {'sec': 1, 'min': 60, 'hour': 3600}

    def wrapper(func):
        @wraps(func)
        def new_func(*args, **kwargs):
            begin = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            exec_time = (end - begin) / multiply[time_form]
            print(f'Duration, {time_form}: {exec_time}')
            return result
        return new_func
    return wrapper


@func_exec_count
# @execution_time()
def summary(x: int, y: int) -> int:
    z = x + y
    return z


@execution_time(time_form='sec')
def main():
    result = 0
    for i in range(1, 10**7):
        result += summary(i, 100)
        print(result)
    print(summary.count, summary.__name__)


main()

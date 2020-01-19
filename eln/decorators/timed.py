# decorators:timed

import time
from functools import wraps

TIMED_OUTPUT = \
    """
    {function}: {time}
    """


def timed(func):
    """
    Martin Heinz
    https://gist.github.com/MartinHeinz/2e2d258b2e6b77280dab04aad9707a7a#file-timeit_decorator-py
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        func_return_val = func(*args, **kwargs)
        end = time.perf_counter()
        print('{0:<10}.{1:<8} : {2:<8}'.format(func.__module__, func.__name__, end - start))
        return func_return_val
    return wrapper

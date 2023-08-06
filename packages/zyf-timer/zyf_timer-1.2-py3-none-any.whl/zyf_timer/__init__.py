import time
from functools import wraps


def timeit_with_digit(digit: int = 4):

    def wrap(func):
        """
        装饰器： 判断函数执行时间
        :param func:
        :return:
        """
        @wraps(func)
        def inner(*args, **kwargs):
            start = time.time()
            ret = func(*args, **kwargs)
            end = time.time() - start
            if end < 60:
                print(f'花费时间:  {end:.{digit}f} secs')
            else:
                min, sec = divmod(end, 60)
                print(f'花费时间:  {round(min)} min  {sec:.{digit}f} secs')
            return ret

        return inner

    return wrap


def timeit(func):
    """
    装饰器： 判断函数执行时间
    :param func:
    :return:
    """
    digit = 4

    @wraps(func)
    def inner(*args, **kwargs):
        start = time.time()
        ret = func(*args, **kwargs)
        end = time.time() - start
        if end < 60:
            print(f'花费时间:  {end:.{digit}f} secs')
        else:
            min, sec = divmod(end, 60)
            print(f'花费时间:  {round(min)} min  {sec:.{digit}f} secs')
        return ret

    return inner

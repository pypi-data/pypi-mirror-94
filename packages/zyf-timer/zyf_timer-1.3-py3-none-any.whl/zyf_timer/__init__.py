import time
from functools import wraps

from prettytable import PrettyTable


def repeat_timeit(repeat: int = 0, number: int = 10, digit: int = 3, print_detail: bool = False, print_table: bool = False):
    def wrap(func):
        """
        装饰器： 判断函数执行时间
        :param func:
        :return:
        """

        @wraps(func)
        def inner(*args, **kwargs):
            func_name, ret = func.__name__, None
            if repeat > 0:
                r = []
                for _ in range(repeat):
                    end, ret = _timeit(func, number, *args, **kwargs)
                    r.append(end)
                min_time, max_time, avg_time = min(r), max(r), sum(r) / repeat
                best_trial_time_string = build_time_print_string(min_time, digit=digit)
                worst_trial_time_string = build_time_print_string(max_time, digit=digit)
                avg_trial_time_string = build_time_print_string(avg_time, digit=digit)
                avg_func_call_time_string = build_time_print_string(avg_time / number, digit)
                if print_table:
                    if print_detail:
                        print(f'Time Spend of {repeat} trials with {number} function calls per trial:')
                        table = PrettyTable(
                            ['Function', 'Best trial', 'Worst trial', 'Average trial', 'Average function call'])
                        table.add_row(
                            [func_name, best_trial_time_string, worst_trial_time_string, avg_trial_time_string,
                             avg_func_call_time_string])
                    else:
                        table = PrettyTable(['Function', 'Average trial', 'Average function call'])
                        table.add_row([func_name, avg_trial_time_string, avg_func_call_time_string])
                    print(table)
                else:
                    if print_detail:
                        print(
                            f'Time Spend of {repeat} trials with {number} function calls per trial:\n\tFunction -> {func_name}: \n\t\tbest: {best_trial_time_string}, worst: {worst_trial_time_string}, average: {avg_trial_time_string}')
                        print(
                            f'Average trial: {avg_trial_time_string}. Average function call: {avg_func_call_time_string}')
                    else:
                        print(
                            f'average trial {avg_trial_time_string}. average function call {avg_func_call_time_string}')

            else:
                end, ret = _timeit(func, number, *args, **kwargs)
                total_time_string = build_time_print_string(end, digit)
                avg_time_string = build_time_print_string(end / number, digit)
                if print_table:
                    if print_detail:
                        print(f'Time Spend of {number} function calls:')
                        table = PrettyTable(['Function', 'Total cost', 'Average cost'])
                        table.add_row([func_name, total_time_string, avg_time_string])
                    else:
                        table = PrettyTable(['Function', 'Average cost'])
                        table.add_row([func_name, avg_time_string])
                    print(table)
                else:
                    if print_detail:
                        print(
                            f'Time Spend of {number} function calls:\n\tFunction -> {func_name}: total {total_time_string}, average {avg_time_string}')
                        print(f'Average: {avg_time_string}')
                    else:
                        print(f'average {avg_time_string}')

            return ret

        return inner

    return wrap


def _timeit(func, number, *args, **kwargs):
    start = time.time()
    num = 1
    while num < number:
        func(*args, **kwargs)
        num += 1
    ret = func(*args, **kwargs)
    end = time.time() - start
    return end, ret


def build_time_print_string(time_seconds: float, digit: int):
    if time_seconds > 60:
        minutes, seconds = divmod(time_seconds, 60)
        return f'{minutes} minutes {seconds:.{digit}f} seconds'
    return f'{time_seconds:.{digit}f} seconds'


def timeit(func):
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
        time_string = build_time_print_string(end, digit=3)
        print(f'Function {func.__name__} -> takes {time_string}')
        return ret

    return inner

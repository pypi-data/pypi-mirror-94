## 计时器-zyf_timer

### 安装

> pip install zyf_timer

### 使用

#### 示例1：timeit

```python
from zyf_timer import timeit

@timeit
def sleep(seconds: int):
    time.sleep(seconds)
```

运行

```bash
>> sleep(1)
Function sleep -> takes 1.001 seconds
```

#### 示例2：repeat_timeit

```python
from zyf_timer import repeat_timeit

@repeat_timeit(number=5)
def list_insert_time_test():
    l = []
    for i in range(10000):
        l.insert(0, i)


@repeat_timeit(repeat=3, number=5)
def list_append_time_test():
    l = []
    for i in range(1000000):
        l.append(i)
    return l


@repeat_timeit(number=5, print_detail=True)
def list_gen_time_test():
    l = [i for i in range(1000000)]
    return l


@repeat_timeit(repeat=3, number=5, print_detail=True)
def list_extend_time_test():
    l = []
    for i in range(1000000):
        l.extend([i])


@repeat_timeit(repeat=3, number=5, print_detail=True, print_table=True)
def list_range_time_test():
    l = list(range(1000000))
```

运行

```bash
>> list_insert_time_test()
Function list_insert_time_test -> 5 function calls: average takes 0.097 seconds

>> list_append_time_test()
Function list_append_time_test -> 3 trials 5 function calls: average trial 3.269 seconds. average function call 0.654 seconds

>> list_gen_time_test()
Time Spend of 5 function calls:
	Function -> list_gen_time_test: total 1.550 seconds, average 0.310 seconds
Average: 0.310 seconds

>> list_extend_time_test()
Time Spend of 3 trials with 5 function calls per trial:
	Function -> list_extend_time_test: 
		best: 3.289 seconds, worst: 3.626 seconds, average: 3.442 seconds
Average trial: 3.442 seconds. Average function call: 0.688 seconds

>> list_range_time_test()
Time Spend of 3 trials with 5 function calls per trial:
+----------------------+---------------+---------------+---------------+-----------------------+
|       Function       |   Best trial  |  Worst trial  | Average trial | Average function call |
+----------------------+---------------+---------------+---------------+-----------------------+
| list_range_time_test | 0.640 seconds | 0.714 seconds | 0.677 seconds |     0.135 seconds     |
+----------------------+---------------+---------------+---------------+-----------------------+
```


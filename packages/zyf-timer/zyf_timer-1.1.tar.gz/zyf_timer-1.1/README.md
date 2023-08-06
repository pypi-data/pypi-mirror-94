### 计时器-zyf_timer

#### 安装

> pip install zyf_timer

#### 使用

```python
from zyf_timer.timer import timeit

@timeit
def main():
    time.sleep(1)
    ...
```

设置保留位数，默认保留两位小数

```python
from zyf_timer.timer import timeit_with_digit

@timeit_with_digit(digit=4)
def main():
    time.sleep(1)
    ...
```


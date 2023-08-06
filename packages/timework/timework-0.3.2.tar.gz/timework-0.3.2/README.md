# timework

[![PyPI](https://img.shields.io/pypi/v/timework)](https://pypi.org/project/timework/)
[![CodeFactor](https://www.codefactor.io/repository/github/bugstop/python-timework/badge)](https://www.codefactor.io/repository/github/bugstop/python-timework)
[![Coverage Status](https://coveralls.io/repos/github/bugstop/python-timework/badge.svg?branch=master)](https://coveralls.io/github/bugstop/python-timework?branch=master)
[![platform](https://img.shields.io/badge/platform-linux%20%7C%20macos%20%7C%20windows-red)](https://github.com/bugstop/python-timework)

measure / limit the function execution time, cross-platform

<!--
python -m pip install --upgrade build
python -m build
python -m pip install --user --upgrade twine
python -m twine upload dist/*
-->

## Install

```bash
pip install timework
```

## Usage

```python
import timework as tw
```

### Statement `with`

#### timework.Stopwatch

**Todo**

### Decorator `@`

**Todo:** read docstrings and tests for more details

#### timework.timer

> measuring the execution time.

```python
import logging

@tw.timer(logging.warning)
def timer_demo_a():
    i = 0
    while i < 2 ** 23:
        i += 1
    return i

@tw.timer(print, detail=True)
def timer_demo_b():
    i = 0
    while i < 2 ** 24:
        i += 1
    return i
```
```python
a = timer_demo_a()
b = timer_demo_b()

print(a, b)
```
```
WARNING:root:timer_demo_a: 0.496672 seconds used
START:  Tue Feb 18 15:06:45 2020
FINISH: Tue Feb 18 15:06:46 2020
timer_demo_b: 0.989352 seconds used
8388608 16777216
```

#### timework.limit

> limiting the execution time.

**`timework.TimeError`** only contains:

- `TimeError.message` ***string,*** <*decorated function name*\>: \<*timeout*\> seconds exceeded
- `TimeError.result` ***None,*** *unused*
- `TimeError.detail` ***None,*** *unused*

```python
@tw.limit(3)
def limit_demo(m):
    i = 0
    while i < 2 ** m:
        i += 1
    return i
```
```python
try:
    s = limit_demo(4)
except tw.TimeError as e:
    print(e)
else:
    print('result:', s)

try:
    s = limit_demo(30)
except tw.TimeError as e:
    print(e)
else:
    print('result:', s)
```
```
result: 16
limit_demo: 3 seconds exceeded
```

## License

MIT License &copy; <a href="https://github.com/bugstop" style="color: black !important; text-decoration: none !important;">bugstop</a>

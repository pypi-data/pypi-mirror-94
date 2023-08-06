from . import timework as tw

import time
from random import randint


@tw.timer(print, detail=True)
def timer_demo(s):
    """
    output example:
      [TIMEWORK] Start:  Mon Feb  8 03:35:06 2021
      [TIMEWORK] Finish: Mon Feb  8 03:35:08 2021
      [TIMEWORK] timer_demo_a used: 00:00:02.406
    """
    time.sleep(s / 10)
    return s * 2


@tw.limit(3)
def limit_demo(m):
    """
    if not timeout:
      work as normal
    If timed out:
      raise TimeError
    """
    i = 0
    while i < 2 ** m:
        i += 1
    return i


def test_timer():
    for _ in range(10):
        d = randint(10, 25)
        x = timer_demo(d)
        assert x == 2 * d


def test_limit():
    for _ in range(10):
        d = randint(15, 35)
        try:
            rc = limit_demo(d)
        except tw.TimeoutException as e:
            assert str(e).startswith('[TIMEWORK] limit_demo')
        else:
            assert rc == 2 ** d


def test_errors():
    try:
        timer_demo('string')
    except Exception as e:
        assert isinstance(e, TypeError)

    try:
        limit_demo('string')
    except Exception as e:
        assert isinstance(e, TypeError)

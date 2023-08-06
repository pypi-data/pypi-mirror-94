from . import timework as tw

import re
from random import randint


@tw.timer(print, detail=True)
def timer_demo_a(m):
    i = 0
    while i < 2 ** m:
        i += 1
    return i


@tw.timer(timeout=1)
def timer_demo_b(m):
    i = 0
    while i < 2 ** m:
        i += 1
    return i


@tw.timer(timeout=-1)
def timer_demo_c(m):
    i = 0
    while i < 2 ** m:
        i += 1
    return i


@tw.limit(3)
def limit_demo(m):
    i = 0
    while i < 2 ** m:
        i += 1
    return i


def test_timer_a():
    for _ in range(10):
        d = randint(10, 25)
        x = timer_demo_a(d)
        assert x == 2 ** d


def test_timer_b():
    for _ in range(10):
        d = randint(10, 25)
        try:
            c = timer_demo_b(d)
        except tw.TimeError as e:
            assert e.message.startswith('timer_demo_b')
            assert re.match(r'^.*:\s(\d|\.)+ seconds used$', e.message) is not None
            assert e.result == 2 ** d
        else:
            assert c == 2 ** d


def test_timer_c():
    for _ in range(10):
        t = -1
        d = randint(10, 25)
        try:
            timer_demo_c(d)
        except tw.TimeError as e:
            t = e.result
        finally:
            assert t == 2 ** d


def test_limit():
    for _ in range(10):
        d = randint(15, 35)
        try:
            s = limit_demo(d)
        except tw.TimeError as e:
            assert isinstance(e, tw.TimeError)
            assert re.match(r'^.*:\s(\d|\.)+ seconds exceeded$', e.message) is not None
        else:
            assert s == 2 ** d


def test_errors():
    try:
        timer_demo_b('2')
    except Exception as e:
        assert isinstance(e, TypeError)

    try:
        limit_demo('2')
    except Exception as e:
        assert isinstance(e, TypeError)

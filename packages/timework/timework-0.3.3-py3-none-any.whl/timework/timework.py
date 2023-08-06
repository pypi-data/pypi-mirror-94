import time
import functools
from math import modf
from typing import Callable
from threading import Thread


def nil(*_, **__):
    """Black hole."""


def sec_to_hms(sec: float) -> str:
    ms, s = modf(sec)
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    hms = "%02d:%02d:%02d.%03.0f" % (h, m, s, ms * 1000)
    return hms


def hms_to_sec(hms: str) -> float:
    h, m, s, ms = map(int, hms.replace('.', ':').split(':'))
    sec = h * 3600 + m * 60 + s + ms * 0.001
    return sec


class TimeoutException(Exception):
    """Exceptions for timeouts."""


def timer(output: Callable = nil, *, detail: bool = False):
    """A decorator. Measuring the execution time.

    The wrapper function measures the execution time of the function that is being
    decorated. The output argument is used to log messages, basically the wrapper
    function will pass the start time, end time, and execution time message to it as
    strings. Whether to pass start time and end time message is controlled by detail
    argument. This argument must be passed using keywords.

    Typical usage examples:

        @timer(logging.warning)
        def your_function():
            ...


    Args:
        output: A function object that specifies where to log messages.
                For example: print. timework.nil does not log messages.
        detail: A boolean value, whether to print start and end time.

    Returns:
        Exactly the return values of the inner function just as normal.
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if detail:
                t = time.asctime(time.localtime(time.time()))
                output('[TIMEWORK] Start:  {}'.format(t))

            initial = time.time()
            rc = func(*args, **kwargs)
            final = time.time()
            used = final - initial

            if detail:
                t = time.asctime(time.localtime(time.time()))
                output('[TIMEWORK] Finish: {}'.format(t))

            s = '[TIMEWORK] {} used: {}' \
                .format(func.__name__, sec_to_hms(used))
            output(s)

            return rc

        return wrapper

    return decorator


def limit(timeout: float):
    """A decorator. Limiting the execution time.

    The wrapper function limits the execution time of the function being
    decorated. The timeout argument is used to set timeout (in seconds).
    After that time of processing, raise a TimeError to terminate.

    Typical usage examples:

        @limit(3)
        def your_function():
            ...


    Args:
        timeout: This argument sets the timeout limit of the decorated function.
                 Once the run time of the process reaches [timeout] seconds but
                 not yet finishes, then raise TimeError and stop the inner function.

    Returns:
        Exactly the return values of the inner function just as normal.
        In this case, the process finishes within [timeout] seconds.

    Raises:
        TimeoutException: This error occurs when the inner function runs
                          for [timeout] seconds and still not finishes.
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            rc = TimeoutException(
                '[TIMEWORK] {} used: {}'
                .format(func.__name__, sec_to_hms(timeout)))

            def new_func():
                nonlocal rc
                try:
                    rc = func(*args, **kwargs)
                except Exception as err:
                    rc = err

            t = Thread(target=new_func)
            t.daemon = True
            t.start()
            t.join(timeout)

            if isinstance(rc, Exception):
                raise rc
            else:
                return rc

        return wrapper

    return decorator


class Stopwatch(object):
    def __init__(self, output=print):
        self.output = output
        self._initial = time.time()
        self._start_at = self._initial
        self._pause_at = self._initial
        self._running = False

    def __enter__(self):
        t = time.asctime(time.localtime(time.time()))
        self.output('[TIMEWORK] Start:  {}'.format(t))

        self.restart()
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        if self._running:
            self.stop()

        t = time.asctime(time.localtime(time.time()))
        self.output('[TIMEWORK] Finish: {}'.format(t))

        return self

    def get_sec(self):
        now = time.time()
        split = now - self._start_at
        total = now - self._initial
        return split, total

    def get_hms(self):
        split, total = map(sec_to_hms, self.get_sec())
        return split, total

    def restart(self):
        self._running = True
        self._initial = time.time()
        self._start_at = self._initial

    def pause(self):
        if self._running:
            self._running = False
            self._pause_at = time.time()

    def resume(self):
        if not self._running:
            self._running = True
            offset = time.time() - self._pause_at

            self._initial += offset
            self._start_at += offset

    def split(self):
        current, total = self.get_hms()
        self.output('[TIMEWORK] Split:  {} | {}'
                    .format(total, current))

        self._start_at = time.time()

    def stop(self):
        self._running = False
        current, total = self.get_hms()

        if self._start_at == self._initial:  # no splits
            self.output('[TIMEWORK] Stop:   {}'.format(total))
        else:
            self.output('[TIMEWORK] Stop:   {} | {}'
                        .format(total, current))

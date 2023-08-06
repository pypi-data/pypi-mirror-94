import time
import functools
from threading import Thread
from collections import deque


class Error(Exception):
    """Base class for exceptions in this module."""


class TimeError(Error):
    """Class for timeouts."""

    def __init__(self, message, result=None, detail=None):
        """Timeout information.

        Args:
            message: timeout error message
            result: return values of the function that is being decorated
            detail: more information (if have)
        """
        self.message = message
        self.result = result
        self.detail = detail


def timer(output=None, *, detail: bool = False, timeout: float = 0):
    """A decorator. Measuring the execution time.

    The wrapper function measures the execution time of the function that is being
    decorated. The output argument is used to log messages, basically the wrapper
    function will pass the start time, end time, and execution time message to it as
    strings. Whether to pass start time message and end time message is controlled
    by detail argument. And timeout argument is used to control error messages. The
    last two arguments must been passed using keywords.

    Typical usage examples:

        @timer(logging.warning)
        def your_function_a():
            ...

        @timer(timeout=5)
        def your_function_b():
            ...


    Args:
        output: A function object that specifies where to log messages.
                For example: print.
        detail: A boolean value, whether to print start and end time.
        timeout: Another optional variable controlling errors,
                 if run_time_after_finished > timeout, then raise TimeError.
                 (0: never, -1: always)

    Returns:
        Exactly the return values of the inner function that is being decorated.
        In this case, the process finishes within [timeout] seconds.

    Raises:
        TimeError: This error does not occur until the inner function
                   terminates, but fails to finish within [timeout] seconds.

                   A TimeError object contains:
                       TimeError.message: timeout message
                       TimeError.result: return values
                       TimeError.detail: used run time
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if output is not None and detail:
                t = time.asctime(time.localtime(time.time()))
                output('START:  {}'.format(t))

            start = time.time()
            rc = func(*args, **kwargs)
            end = time.time()

            used = end - start
            s = '{}: {:g} seconds used'.format(func.__name__, used)

            if timeout != 0 and used > timeout:
                e = TimeError(s, rc, used)
                raise e

            if output is not None:
                t = time.asctime(time.localtime(time.time()))
                output(s if not detail else 'FINISH: {}\n{}'.format(t, s))

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
        Exactly the return values of the inner function that is being decorated.
        In this case, the process finishes within [timeout] seconds.

    Raises:
        TimeError: This error occurs when the inner function runs
                   for [timeout] seconds and still not finishes.

                   A TimeError object contains:
                       TimeError.message: timeout message
                       TimeError.result: None (unused)
                       TimeError.detail: None (unused)
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            rc = TimeError('{}: {:g} seconds exceeded'
                           .format(func.__name__, timeout))

            def new_func():
                nonlocal rc
                try:
                    rc = func(*args, **kwargs)
                except Exception as err_:
                    rc = err_

            t = Thread(target=new_func)
            t.daemon = True
            t.start()
            t.join(timeout)

            if isinstance(rc, Exception):
                raise rc

            return rc

        return wrapper

    return decorator

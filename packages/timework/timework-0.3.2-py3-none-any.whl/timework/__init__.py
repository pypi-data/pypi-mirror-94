"""
timework 0.3.2

MIT License © bugstop

PyPI:   https://pypi.org/project/timework/
GitHub: https://github.com/bugstop/python-timework/


measure / limit the function execution time, cross-platform

timework.timer()      - a decorator measuring the execution time
timework.limit()      - a decorator limiting the execution time
timework.Stopwatch()  - a with statement class for stopwatch
"""


from .timework import *

__name__ = 'timework'
__version__ = '0.3.2'
__all__ = ['timer', 'limit', 'Stopwatch']

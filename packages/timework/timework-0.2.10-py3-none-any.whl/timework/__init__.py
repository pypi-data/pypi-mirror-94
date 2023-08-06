"""
timework 0.2.10

MIT License © bugstop

PyPI:   https://pypi.org/project/timework/
GitHub: https://github.com/bugstop/timework-timeout-decorator/


measure / limit the function execution time, cross-platform

timework.timer      - a decorator measuring the execution time.
timework.limit      - a decorator limiting the execution time.
"""


from .timework import *

__name__ = 'timework'
__version__ = '0.2.10'
__all__ = ['timer', 'limit']

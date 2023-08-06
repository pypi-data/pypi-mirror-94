"""Various helping functions"""
from typing import Callable, Iterable
from time import time
from functools import wraps

try:
    from logzero import logger
except ImportError:
    import logging as logger

# =======================================================================
# Class Utitlities
# =======================================================================


class Singleton(type):
    """Singleton Metaclass"""

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(
                *args,
                **kwargs,
            )
        return cls._instances[cls]


# =======================================================================
# Function utitlities
# =======================================================================
def now(
    secs: int = 0,
    mins: int = 0,
    hrs: int = 0,
    days: int = 0,
    milisecond: bool = False,
):
    """
    Get time in Unix
    Args:
        sec : Seconds
        min : Minutes
        hr  : Hours
        day : Days
        milisecond : miliseconds or seconds
    Returns:
        int : unix time
    """
    current = int(time())
    delta = secs * 1 + mins * 60 + hrs * 3600 + days * 3600 * 24
    result = current + delta
    return result * 1000 if milisecond else result


def find(predicate: Callable, items: Iterable, default=None):
    """Find first item in the iterable
    that matches using predicate function
    - A predicate function must always return a boolean value
    """
    return next((x for x in items if predicate(x) is True), default)


def try_except(description: str, propagate=False):
    """Wrapping function in try-except block, allow propagate to upper level"""

    def wrapped(func):
        @wraps(func)
        def inner_wrapped(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as err:
                msg = f"=====>>> {description} <<<======"
                logger.error(msg)
                logger.exception(err)
                logger.error("Args: %s", args)
                if propagate:
                    raise err

        return inner_wrapped

    return wrapped

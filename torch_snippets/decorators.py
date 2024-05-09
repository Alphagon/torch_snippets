# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/decorators.ipynb.

# %% auto 0
__all__ = ["timeit", "io", "check_kwargs_not_none"]

# %% ../nbs/decorators.ipynb 2
from functools import wraps
from .inspector import inspect
from .logger import Info
import time

# %% ../nbs/decorators.ipynb 3
def timeit(func):
    """
    A decorator that measures the execution time of a function.

    Args:
        func (callable): The function to be timed.

    Returns:
        callable: The wrapped function.

    Example:
        @timeit
        def my_function():
            # code to be timed
            pass

        my_function()  # prints the execution time of my_function
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        output = func(*args, **kwargs)
        end = time.time()
        Info(f"{func.__name__} took {end-start:.2f} seconds to execute")
        return output

    return wrapper


def io(func):
    """
    A decorator that inspects the inputs and outputs of a function.

    Args:
        func: The function to be decorated.

    Returns:
        The decorated function.

    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        if len(args) != 0:
            inspect(args, names=["inputs:args"])
        if kwargs != {}:
            inspect(kwargs, names=["inputs:kwargs"])
        output = func(*args, **kwargs)
        inspect(output, names=["outputs"])
        return output

    return wrapper


def check_kwargs_not_none(func):
    """
    A decorator that checks if any keyword argument is None.
    Raises a ValueError if any argument is None.

    Args:
        func: The function to be decorated.

    Returns:
        The decorated function.

    Raises:
        ValueError: If any keyword argument is None.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        for key, value in kwargs.items():
            if value is None:
                raise ValueError(f"Input argument '{key}' cannot be None")
        return func(*args, **kwargs)

    return wrapper

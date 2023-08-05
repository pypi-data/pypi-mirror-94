"""
~ decorators.py

Python decorators are written here, they can be used anywhere in your code.
Example of the use of a decorator:
    @add_method(str)
    def double_last_letter(self)
        return self + self[-1]

"""
from functools import wraps
from timeit import default_timer
from forbiddenfruit import curse


def time_it(func):
    """
    Display the program's execution time of a given function.
    :param func: function called this decorator.
    :return: function
    """
    @wraps(func)
    def _wrapper_time_it(*args, **kwargs):
        start = default_timer()
        result = func(*args, **kwargs)
        end = default_timer()
        delta = end - start
        print(f'Time taken for {func.__name__} is {round(delta, 4)} seconds.')
        return result
    return _wrapper_time_it


def add_method(cls):
    """
    Add method/function to a given class.
    The added method will be available for the instanciated object of this class.
    :param cls: class method
    :return: function
    """
    def decorator(func):
        @wraps(func)
        def _wrapper_add_method(*args, **kwargs):
            return func(*args, **kwargs)

        curse(cls, func.__name__, _wrapper_add_method)
        return func

    return decorator


__all__ = ['time_it', 'add_method']

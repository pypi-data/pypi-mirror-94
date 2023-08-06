import functools
from contextlib import redirect_stdout


class _Log:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        with open(f'func_{self.func.__name__}.log', 'w') as f:
            with redirect_stdout(f):
                result = self.func(*args, **kwargs)
        return result


def log(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return _Log(func)(*args, **kwargs)

    return wrapper
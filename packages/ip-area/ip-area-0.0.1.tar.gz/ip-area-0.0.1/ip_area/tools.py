# -*- coding: utf-8 -*-
from functools import wraps


def try_decorator(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            return None

    return decorator

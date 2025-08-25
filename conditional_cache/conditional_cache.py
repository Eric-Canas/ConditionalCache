from __future__ import annotations
from functools import wraps, _make_key
from circular_dict import CircularDict
from time import time

def _freeze_for_key(obj):
    # Fast-path for hashables
    try:
        hash(obj)
        return obj
    except TypeError:
        pass

    if isinstance(obj, tuple):
        return tuple(_freeze_for_key(x) for x in obj)
    if isinstance(obj, list):
        return tuple(_freeze_for_key(x) for x in obj)
    if isinstance(obj, set):
        return frozenset(_freeze_for_key(x) for x in obj)
    if isinstance(obj, dict):
        # Stable order: sort by key; freeze values
        return frozenset((k, _freeze_for_key(v)) for k, v in sorted(obj.items(), key=lambda kv: kv[0]))
    # Fallback: best-effort stable representation
    return repr(obj)

def _freeze_args_kwargs(args, kwargs):
    frozen_args = tuple(_freeze_for_key(a) for a in args)
    # keep kwargs as dict (as _make_key expects), but freeze the values
    frozen_kwargs = {k: _freeze_for_key(v) for k, v in kwargs.items()}
    return frozen_args, frozen_kwargs


def conditional_lru_cache(maxsize: int=128, maxsize_bytes: int | None = None, typed: bool = False, condition: callable = lambda x: True):
    cache = CircularDict(maxlen=maxsize, maxsize_bytes=maxsize_bytes)

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # create a hashable cache key (helping with unhashable args like lists or dicts)
            f_args, f_kwargs = _freeze_args_kwargs(args, kwargs)
            key = _make_key(f_args, f_kwargs, typed)

            # Attempt to get the cached value
            if key in cache:
                return cache[key]

            # Call the actual function
            result = func(*args, **kwargs)

            # Conditionally cache the result
            if condition(result):
                try:
                    cache[key] = result
                except MemoryError:
                    # Item too large for the byte budget: don't store it
                    pass

            return result

        # Expose a method to remove an item from the cache
        def cache_remove(*args, **kwargs):
            f_args, f_kwargs = _freeze_args_kwargs(args, kwargs)
            key = _make_key(f_args, f_kwargs, typed)
            cache.pop(key, None)  # Use pop to avoid KeyError if the key is not present

        wrapper.cache_remove = cache_remove
        # Expose a method to clear the full cache
        wrapper.cache_clear = lambda: cache.clear()

        return wrapper

    return decorator

def conditional_ttl_cache(maxsize: int = 128, maxsize_bytes: int | None = None, typed: int = False, ttl: int = 60, condition: callable = lambda x: True):
    cache = CircularDict(maxlen=maxsize, maxsize_bytes=maxsize_bytes)

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # create a hashable cache key
            f_args, f_kwargs = _freeze_args_kwargs(args, kwargs)
            key = _make_key(f_args, f_kwargs, typed)

            # Attempt to get the cached value
            if key in cache:
                value_timestamp, value = cache[key]
                if time() - value_timestamp < ttl:
                    return value
                else:
                    # If the item has expired, remove it from the cache
                    del cache[key]

            # Call the actual function
            result = func(*args, **kwargs)

            # Conditionally cache the result
            if condition(result):
                # Store with current timestamp
                try:
                    cache[key] = (time(), result)
                except MemoryError:
                    # Item too large for the byte budget: don't store it
                    pass

            return result

        # Expose a method to remove an item from the cache
        def cache_remove(*args, **kwargs):
            f_args, f_kwargs = _freeze_args_kwargs(args, kwargs)
            key = _make_key(f_args, f_kwargs, typed)
            if key in cache:
                del cache[key]

        wrapper.cache_remove = cache_remove
        # Expose a method to clear the full cache
        wrapper.cache_clear = lambda: cache.clear()

        return wrapper

    return decorator

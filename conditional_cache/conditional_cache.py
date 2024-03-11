from functools import wraps, _make_key
from circular_dict import CircularDict

def conditional_lru_cache(maxsize=128, typed=False, condition_func=lambda x: True):
    cache = CircularDict(maxlen=maxsize)

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # create a hashable cache key
            key = _make_key(args, kwargs, typed)

            # Attempt to get the cached value
            if key in cache:
                return cache[key]

            # Call the actual function
            result = func(*args, **kwargs)

            # Conditionally cache the result
            if condition_func(result):
                cache[key] = result

            return result

        # Expose a method to remove an item from the cache
        def cache_remove(*args, **kwargs):
            key = _make_key(args, kwargs, typed)
            cache.pop(key, None)  # Use pop to avoid KeyError if the key is not present


        wrapper.cache_remove = cache_remove
        # Expose a method to clear the full cache
        wrapper.cache_clear = lambda: cache.clear()

        return wrapper

    return decorator

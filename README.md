# ConditionalCache
<img alt="ConditionalCache" title="ConditionalCache" src="https://raw.githubusercontent.com/Eric-Canas/ConditionalCache/main/resources/logo.png" width="20%" align="left">

**ConditionalCache** is a set of _decorators_, that provide **conditional function memoization** and **selective cache clearing**.

It works under the same interface that most standard cache decorators like [functools.lru_cache](https://docs.python.org/es/3/library/functools.html#functools.lru_cache) or [cachetools.ttl_cache](https://cachetools.readthedocs.io/en/latest/#cachetools.TTLCache), but unlocking a new `condition` parameter, that will determine if the function result is _memoized_ or not. This feature allows for more granular control over caching behavior, useful for those use cases where we want to store the output only when certain conditions are met. As for example when checking existence in databases.

## Installation

To install **ConditionalCache** simply run:

```bash
pip install conditional-cache
```

## Usage
Working with **ConditionalCache** is as simple and straight-forward as using [functools.lru_cache](https://docs.python.org/es/3/library/functools.html#functools.lru_cache), as it works under the same interface.

```python
from conditional_cache import lru_cache

# Memoize the returned element only when it is different than "Not Found"
@lru_cache(maxsize=64, condition=lambda db_value: db_value != "Not Found")
def element_exists_in_db(element_id: int) -> str:

  print(f"Asked to DB: {element_id}")
  # For the example let's consider that even elements exists.
  return "Found" if element_id % 2 == 0 else "Not Found"
```

When we will call this function, it will be execute **only once** for even numbers, and always for odds.

```python
# Will be executed, and not memoized
print(f"Returned: {element_exists_in_db(element_id=1)}")
# Will be executed again
print(f"Returned: {element_exists_in_db(element_id=1)}\n")

# Will be executed and memoized
print(f"Returned: {element_exists_in_db(element_id=2)}")
# Will return the memoized result without executing again
print(f"Returned: {element_exists_in_db(element_id=2)}")
```

```bash
>> Asked to DB: 1
>> Returned: Not Found
>> Asked to DB: 1
>> Returned: Not Found

>> Asked to DB: 2
>> Returned: Found
>> Returned: Found
```

If during your execution, you perform an action that invalidate a given function result, you can actively remove that element cache:

```python
# Will return the result that was memoized before
print(f"Returned: {element_exists_in_db(element_id=2)}\n")
# Remove the element from the cache
element_exists_in_db.cache_remove(element_id=2)

# Will be executed again and memoized
print(f"Returned: {element_exists_in_db(element_id=2)}")
# Will return the memoized result
print(f"Returned: {element_exists_in_db(element_id=2)}")
```

```bash
>> Returned: Found

>> Asked to DB: 2
>> Returned: Found
>> Returned: Found
```

### Controlling cache size by memory
In addition to `maxsize` (number of elements), you can also limit the cache by **memory usage** with `maxsize_bytes`.

```python
from conditional_cache import lru_cache

@lru_cache(maxsize_bytes=1024)  # keep up to ~1 KB of cached data
def heavy_query(x: int) -> str:
    print("Executed:", x)
    return "X" * (x * 100)

heavy_query(1)   # Cached
heavy_query(10)  # May evict older entries if too large
```

This way you can avoid **overflowing** your memory if you need to cache large objects like images. If a single result is **too large** to ever fit in the cache, it will just not be stored.

### Time-based expiration (TTL)
Use `ttl_cache` when you want cached entries to automatically expire after a given number of seconds.

```python
import time
from conditional_cache import ttl_cache

@ttl_cache(ttl=3, maxsize=64, condition=lambda r: r is not None)
def fetch_user(user_id: int) -> dict | None:
    print("Fetching:", user_id)
    return {"id": user_id}

fetch_user(1)      # Executed and cached
time.sleep(1)
fetch_user(1)      # Retrieved from cache
time.sleep(3)
fetch_user(1)      # Expired -> executed again
```

### Unhashable arguments
Unlike `functools`, **ConditionalCache** supports common unhashable types like `list`, `dict`, or `set` as arguments. They are transparently converted to hashable equivalents to avoid headaches.

```python
from conditional_cache import lru_cache

@lru_cache(maxsize=32)
def stringify(a: list, b: dict) -> str:
    print("Executed:", a, b)
    return str(a) + str(b)

print(stringify([1,2,3], {"x": 42}))
print(stringify([1,2,3], {"x": 42}))  # retrieved from cache
```

## API Reference

### conditional_cache.lru_cache(maxsize: int = 128, maxsize_bytes: int | None = None, typed: bool = False, condition: callable = lambda x: True)
An _Least Recently Used_ Cache. It works the same way that [functools.lru_cache](https://docs.python.org/es/3/library/functools.html#functools.lru_cache) but accepting **conditional storage** and **selective item removing** through <decorated_function>.cache_remove(**args)

- `maxsize`: **int**. The maximum amount of elements to keep cached. Once the cache is full, new elements will start to override oldest ones.
- `maxsize_bytes`: **int | None**. The maximum amount of memory (in bytes, as estimated by `sys.getsizeof`) to keep cached. Useful when caching large objects. If a single item is larger than this budget, it will simply not be cached.
- `typed`: **bool**. Works the same way that [functools.lru_cache](https://docs.python.org/es/3/library/functools.html#functools.lru_cache). If `True`, function arguments of different types will be cached separately.
- `condition`: **callable**. It must be a function that receives a single parameter as input (the output of the _decorated_ method) and returns a `boolean`. `True` if the result should be cached or `False` if it should not.

### conditional_cache.ttl_cache(maxsize: int = 128, maxsize_bytes: int | None = None, typed: bool = False, ttl: int = 60, condition: callable = lambda x: True)
A _Time-To-Live_ cache. Behaves like `lru_cache` with the same conditional storage and selective removal features, but cached entries automatically expire after `ttl` seconds.

- `maxsize`: **int**. Maximum number of elements to keep cached.
- `maxsize_bytes`: **int | None**. Maximum memory budget for cached data. Items larger than this budget are not cached.
- `typed`: **bool**. If `True`, function arguments of different types are cached separately.
- `ttl`: **int**. Time-to-live in seconds for each cached entry.
- `condition`: **callable**. Receives the function output and returns `True` if it should be cached.

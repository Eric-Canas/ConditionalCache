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
Working with **ConditionalCache** is as simple and straight-forward as using as using [functools.lru_cache](https://docs.python.org/es/3/library/functools.html#functools.lru_cache), as it works under the same interface (and is in fact interoperable).

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

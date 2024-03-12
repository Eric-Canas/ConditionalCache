# ConditionalCache

**ConditionalCache** is a set of decorators, that provide **conditional function memoization** and **selective cache clearing**.

It works the same way that most standard memoization decorators like [functools.lru_cache](https://docs.python.org/es/3/library/functools.html#functools.lru_cache) or [cachetools.ttl_cache](https://cachetools.readthedocs.io/en/latest/#cachetools.TTLCache), but unlocking a new `condition` parameter

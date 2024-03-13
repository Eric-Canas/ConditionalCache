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

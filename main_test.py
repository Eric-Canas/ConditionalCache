from conditional_cache import conditional_lru_cache as lru_cache, conditional_ttl_cache as ttl_cache

# Example usage
@ttl_cache(maxsize=32, ttl=5, condition=lambda result: result == True)
def foo(item_id: int) -> bool:
    # Simulate a database query
    print(f"Executed for: {item_id}")
    return item_id % 2 == 0  # Only even IDs will be cached


# Testing the decorator
print("=== TTL CACHE DEMO ===")
print(foo(item_id=1))  # Not cached
print(foo(item_id=2))  # Cached
print(foo(item_id=2))  # From cache
print(foo(item_id=3))  # Not cached
print(foo(item_id=3))  # Not cached
print(foo(item_id=4))  # Cached
print(foo(item_id=4))  # From cache
print(foo(item_id=2))  # From cache
foo.cache_remove(item_id=2)  # Remove the result from cache
print(foo(item_id=2))  # Cached again
print(foo(item_id=2))  # From cache
print(foo(item_id=4))  # From cache


# === Minimal test for maxsize_bytes ===
print("\n=== LRU CACHE WITH maxsize_bytes TEST ===")

@lru_cache(maxsize=None, maxsize_bytes=200, condition=lambda result: True)
def bar(x: str) -> str:
    print(f"Executed for: {x}")
    return x

# Fill with small items (should fit)
bar("a"*1)
bar("b"*1)
print("Cache contains:", list(bar.__closure__[0].cell_contents.keys()))  # internal peek

# Add a large item that should not fit (not cached)
bar("long_string_value_exceeding"*100)
# Add another small item (should fit deleting previous)
bar("c"*10)
print("After adding large and another small item, cache contains:", list(bar.__closure__[0].cell_contents.keys()))  # internal peek


# Unhashable args test
print("\n=== UNHASHABLE ARGS TEST ===")
@lru_cache(maxsize=32, condition=lambda result: True)
def baz(a: list, b: dict) -> str:
    print(f"Executed for: {a}, {b}")
    return str(a) + str(b)

# explode
try:
    baz([1, 2, 3], {'key': 'value'})
except TypeError as e:
    print("Caught expected TypeError for unhashable args:", e)
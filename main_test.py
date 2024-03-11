from conditional_cache import conditional_lru_cache

# Example usage
@conditional_lru_cache(maxsize=32, condition_func=lambda result: result == True)
def foo(item_id: int) -> bool:
    # Simulate a database query
    print(f"Executed for: {item_id}")
    return item_id % 2 == 0  # Only even IDs will be cached

# Testing the decorator
print(foo(item_id=1))  # This call's result is not cached due to condition
print(foo(item_id=2))  # This call's result is cached
print(foo(item_id=2))  # This call retrieves the result from cache
print(foo(item_id=3))  # This call's result is not cached due to condition
print(foo(item_id=3))  # This call's result is not cached due to condition
print(foo(item_id=4))  # This call retrieves the result from cache
print(foo(item_id=4))  # This call retrieves the result from cache
print(foo(item_id=2))  # This call retrieves the result from cache
foo.cache_remove(item_id=2)  # Remove the result from cache
print(foo(item_id=2))  # This call's result is cached
print(foo(item_id=2))  # This call's result is retrieved from cache
print(foo(item_id=4))  # This call retrieves the result from cache
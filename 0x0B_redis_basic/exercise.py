#!/usr/bin/env python3
"""Redis basic: module providing a Cache class to store and retrieve values,
with call count tracking via Redis.
"""
from typing import Callable, Optional, TypeVar, Union
from uuid import uuid4
import functools

import redis

T = TypeVar("T")


def count_calls(method: Callable) -> Callable:
    """Decorator to count how many times a method is called.

    It uses the Redis INCR command to increment a counter stored under the
    method's qualified name (``__qualname__``).
    """

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


class Cache:
    """Simple cache wrapper over a Redis client with call counting."""

    def __init__(self) -> None:
        """Initialize the Redis client and flush the database."""
        self._redis: redis.Redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store data in Redis under a random UUID key and return the key."""
        key: str = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(
        self, key: str, fn: Optional[Callable[[bytes], T]] = None
    ) -> Optional[Union[bytes, T]]:
        """Retrieve a value by key and optionally convert its type."""
        data = self._redis.get(key)
        if data is None:
            return None
        return fn(data) if fn is not None else data

    def get_str(self, key: str) -> Optional[str]:
        """Retrieve a UTF-8 decoded string for the given key, or None."""
        return self.get(key, fn=lambda d: d.decode("utf-8"))  # type: ignore[return-value]

    def get_int(self, key: str) -> Optional[int]:
        """Retrieve an integer for the given key, or None."""
        return self.get(key, fn=int)  # type: ignore[return-value]


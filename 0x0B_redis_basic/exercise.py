#!/usr/bin/env python3
"""
Redis basic: module providing a Cache class to store and retrieve values.

This module defines a Cache class that connects to a local Redis server
and offers methods to store arbitrary data under a random key and get it
back, optionally converting it to the original Python type.
"""
from typing import Callable, Optional, TypeVar, Union
from uuid import uuid4

import redis

T = TypeVar("T")


class Cache:
    """Simple cache wrapper over a Redis client.

    Upon initialization, it creates a Redis client connected to the
    default local server and flushes the current database to provide a
    clean state for exercises.
    """

    def __init__(self) -> None:
        """Initialize the Redis client and flush the database."""
        self._redis: redis.Redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store data in Redis under a random UUID key and return the key."""
        key: str = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(
        self, key: str, fn: Optional[Callable[[bytes], T]] = None
    ) -> Optional[Union[bytes, T]]:
        """Retrieve a value by key and optionally convert its type.

        If the key does not exist, return None. Otherwise return the raw
        bytes from Redis, or the value transformed by ``fn`` when provided.
        """
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

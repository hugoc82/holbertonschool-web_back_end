#!/usr/bin/env python3
"""
Redis basic: module providing a Cache class.
"""
import redis
from typing import Union
from uuid import uuid4


class Cache:
    """Simple cache wrapper over a Redis client."""

    def __init__(self) -> None:
        """Initialize the Redis client and flush the DB."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store data in Redis and return the key."""
        key = str(uuid4())
        self._redis.set(key, data)
        return key

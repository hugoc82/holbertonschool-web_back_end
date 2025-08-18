#!/usr/bin/env python3
"""
Fichier principal
"""
import redis
from exercise import Cache

cache = Cache()
data = b"bonjour"
key = cache.store(data)
print("Clé générée :", key)

local_redis = redis.Redis()
print("Valeur retrouvée :", local_redis.get(key))

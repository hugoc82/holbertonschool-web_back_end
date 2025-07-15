#!/usr/bin/python3
"""1. FIFO caching"""

from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """FIFOCache class that uses FIFO caching algorithm"""

    def __init__(self):
        """Initialize the cache"""
        super().__init__()  # appel du constructeur parent
        self.queue = []     # pour garder l'ordre des clés insérées

    def put(self, key, item):
        """Add an item in the cache using FIFO algorithm"""
        if key is None or item is None:
            return

        if key not in self.cache_data:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                # Retirer la première clé entrée (FIFO)
                discarded_key = self.queue.pop(0)
                del self.cache_data[discarded_key]
                print(f"DISCARD: {discarded_key}")

            self.queue.append(key)

        # Même si la clé existe, on remplace juste sa valeur
        self.cache_data[key] = item

    def get(self, key):
        """Get an item by key"""
        return self.cache_data.get(key, None)

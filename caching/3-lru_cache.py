#!/usr/bin/python3
"""3. LRU caching"""

from base_caching import BaseCaching


class LRUCache(BaseCaching):
    """LRUCache class that uses LRU caching algorithm"""

    def __init__(self):
        """Initialize"""
        super().__init__()
        self.usage_order = []  # Liste des clés dans l’ordre d’utilisation

    def put(self, key, item):
        """Add an item in the cache using LRU algorithm"""
        if key is None or item is None:
            return

        if key in self.cache_data:
            self.cache_data[key] = item
            self.usage_order.remove(key)
            self.usage_order.append(key)
        else:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                lru_key = self.usage_order.pop(0)  # Le plus ancien
                del self.cache_data[lru_key]
                print(f"DISCARD: {lru_key}")
            self.cache_data[key] = item
            self.usage_order.append(key)

    def get(self, key):
        """Get an item by key"""
        if key is None or key not in self.cache_data:
            return None

        # Mise à jour de la position dans la file d’utilisation
        self.usage_order.remove(key)
        self.usage_order.append(key)
        return self.cache_data[key]

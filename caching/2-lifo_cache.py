#!/usr/bin/python3
"""2. LIFO caching"""

from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """LIFOCache class that uses LIFO caching algorithm"""

    def __init__(self):
        """Initialize the cache"""
        super().__init__()
        self.last_key = None  # Pour suivre la dernière clé insérée

    def put(self, key, item):
        """Add an item in the cache using LIFO algorithm"""
        if key is None or item is None:
            return

        if key not in self.cache_data:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                # Supprime la dernière clé insérée
                if self.last_key in self.cache_data:
                    del self.cache_data[self.last_key]
                    print(f"DISCARD: {self.last_key}")

        # Ajouter ou remplacer l’élément
        self.cache_data[key] = item
        self.last_key = key  # mettre à jour la dernière clé insérée

    def get(self, key):
        """Get an item by key"""
        return self.cache_data.get(key, None)

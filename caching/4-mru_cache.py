#!/usr/bin/python3
"""4. MRU caching"""

from base_caching import BaseCaching


class MRUCache(BaseCaching):
    """MRUCache class that uses MRU caching algorithm"""

    def __init__(self):
        """Initialize"""
        super().__init__()
        self.usage_order = []  # Liste des clés selon ordre d’utilisation

    def put(self, key, item):
        """Add an item in the cache using MRU algorithm"""
        if key is None or item is None:
            return

        if key in self.cache_data:
            # Mise à jour de la valeur et de la position dans l’ordre d’utilisation
            self.cache_data[key] = item
            self.usage_order.remove(key)
            self.usage_order.append(key)
        else:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                # Supprimer la clé la plus récemment utilisée
                mru_key = self.usage_order.pop()  # Dernier utilisé
                del self.cache_data[mru_key]
                print(f"DISCARD: {mru_key}")

            self.cache_data[key] = item
            self.usage_order.append(key)

    def get(self, key):
        """Get an item by key and mark as recently used"""
        if key is None or key not in self.cache_data:
            return None

        # Met à jour la position dans la file d’usage
        self.usage_order.remove(key)
        self.usage_order.append(key)
        return self.cache_data[key]

#!/usr/bin/python3
"""0. Basic dictionary caching"""

from base_caching import BaseCaching


class BasicCache(BaseCaching):
    """BasicCache class that inherits from BaseCaching
    - No limit on the number of items
    """

    def put(self, key, item):
        """Assign the item to the cache dictionary for the key"""
        if key is None or item is None:
            return
        self.cache_data[key] = item

    def get(self, key):
        """Return the value in cache_data linked to key"""
        return self.cache_data.get(key, None)

#!/usr/bin/python3
"""BaseCaching module"""

class BaseCaching():
    """Base class for caching systems"""
    MAX_ITEMS = 4

    def __init__(self):
        """Initialize the cache"""
        self.cache_data = {}

    def print_cache(self):
        """Print the cache data"""
        print("Current cache:")
        for key in self.cache_data:
            print(f"{key}: {self.cache_data[key]}")

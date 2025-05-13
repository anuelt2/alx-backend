#!/usr/bin/env python3
""" LIFOCache module
"""

from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """ LIFO caching system
    """
    def __init__(self):
        """ Initialize LIFO cache
        """
        super().__init__()
        self.order = []

    def put(self, key, item):
        """ Add an item to the cache
        """
        if key is None or item is None:
            return
        if key not in self.cache_data:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                last_item = self.order.pop()
                del self.cache_data[last_item]
                print("DISCARD:", last_item)

        self.cache_data[key] = item

        if key not in self.order:
            self.order.append(key)

    def get(self, key):
        """ Get an item by key from the cache
        """
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data[key]

#!/usr/bin/env python3
""" LFUCache module
"""

from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """ LFU caching system
    """
    def __init__(self):
        """ Initialize LFU cache
        """
        super().__init__()
        self.order = []
        self.frequency = {}

    def put(self, key, item):
        """ Add an item to the cache
        """
        if key is None or item is None:
            return

        if key in self.cache_data:
            self.cache_data[key] = item
            self.frequency[key] += 1
            self.order.remove(key)
            self.order.append(key)
        else:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                min_frequency = min(self.frequency.values())

                remove_list = [key for key in self.order
                               if self.frequency[key] == min_frequency]

                lfu_key = remove_list[0]
                del self.cache_data[lfu_key]
                del self.frequency[lfu_key]
                self.order.remove(lfu_key)
                print("DISCARD:", lfu_key)

            self.cache_data[key] = item
            self.frequency[key] = 1
            self.order.append(key)

    def get(self, key):
        """ Get an item by key from the cache
        """
        if key is None or key not in self.cache_data:
            return None

        self.frequency[key] += 1
        self.order.remove(key)
        self.order.append(key)

        return self.cache_data[key]

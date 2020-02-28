# Author: Matthew Manning
# Student ID: #000967779

class HashTable:
    # Hash Table constructor with optional size parameter
    # All buckets assigned an empty list
    def __init__(self, default_size=10):
        self.table = []
        for i in range(default_size):
            self.table.append([])

    # Function to find which bucket is used
    # O(1) time complexity
    def find_hash(self, key):
        bucket = key % len(self.table)
        return bucket

    # Add new item into hash table
    # O(N) space time complexity
    def add(self, key, value):
        bucket = self.table[self.find_hash(key)]
        key_value = [key, value]
        bucket.append(key_value)

    # Search for item in hash table
    # O(1) time complexity
    def search(self, key):
        bucket = self.find_hash(key)
        if self.table[bucket] is not None:
            for i in self.table[bucket]:
                if i[0] == key:
                    return i[1]
        return None

    # Delete item from hash table based off key entered (not used)
    # O(N) time complexity
    def delete(self, key):
        bucket = self.find_hash(key)

        if self.table[bucket] is None:
            return False
        for i in range(0, len(self.table[bucket])):
            if self.table[bucket][i][0] == key:
                self.table[bucket].pop(i)
                return True

    # Sort the items in hashtable by key rather than by bucket
    # O(N^2) space-time complexity
    def sort_keys(self):
        sorted_packages = []
        for j in range(len(self.table)):
            for i in self.table[j]:
                sorted_packages.append(i[0])
        return sorted(sorted_packages)









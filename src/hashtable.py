# '''
# Linked List hash table key/value pair
# '''
class LinkedPair:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


class HashTable:
    """
    A hash table that has `capacity` buckets
    that accepts string keys
    """

    def __init__(self, capacity):
        self.capacity = capacity  # Number of buckets in the hash table
        self.count = 0  # Number of buckets used in the hash table

        # For shrinking only when current size above initial size
        self.initial_size = capacity

        self.storage = [None] * capacity

    def _hash(self, key):
        """
        Hash an arbitrary key and return an integer.

        You may replace the Python hash with DJB2 as a stretch goal.
        """
        return hash(key)

    def _hash_djb2(self, key):
        """
        Hash an arbitrary key using DJB2 hash

        OPTIONAL STRETCH: Research and implement DJB2
        """
        pass

    def _hash_mod(self, key):
        """
        Take an arbitrary key and return a valid integer index
        within the storage capacity of the hash table.
        """
        return self._hash(key) % self.capacity

    def insert(self, key, value):
        """
        Store the value with the given key.
        """

        # Possibilities
        # 1. Key already exists
        # 2. Key already exists and first node does not match key
        # 3. Key does not exist

        hashed_key = self._hash_mod(key)

        if self.storage[hashed_key]:
            # hashed key already exists
            node = self.storage[hashed_key]

            if node.key == key:
                # Update value of existing key
                node.value = value
            else:
                # Traverse linked list to find matching key
                # Append new node if not found
                while node.next:
                    # Move to next node in list
                    node = node.next
                    if node.key == key:
                        # Update value of existing key
                        node.value = value
                        break

                # Add new node since we didn't find matching key above
                node.next = LinkedPair(key, value)
                self.count += 1
        else:
            self.storage[hashed_key] = LinkedPair(key, value)
            self.count += 1

        # Will resize hash table based on usage factor
        if self.count / self.capacity > 0.7:
            self.resize(direction=1)

    def remove(self, key):
        """
        Remove the value stored with the given key.

        Print a warning if the key is not found.
        """

        hashed_key = self._hash_mod(key)

        if self.storage[hashed_key]:
            # Key exists, check first node if it matches provided string key
            if self.storage[hashed_key].key == key:
                self.storage[hashed_key] = None
                self.count -= 1
            else:
                # Find key and remove it
                node = self.storage[hashed_key]

                while node.next:
                    if node.next.key == key:
                        # Key found, remove reference
                        node.next = None
                        self.count -= 1
                    else:
                        node = node.next
        else:
            # Key not found
            print("Key not found")

        # Will resize hash table based on usage factor
        # From README: "This should only occur if the HashTable has been resized past the initial size."
        if self.count / self.capacity < 0.2 and self.capacity > self.initial_size:
            self.resize(direction=-1)

    def retrieve(self, key):
        """
        Retrieve the value stored with the given key.

        Returns None if the key is not found.
        """

        hashed_key = self._hash_mod(key)

        if self.storage[hashed_key]:
            # Key is valid index
            if self.storage[hashed_key].key == key:
                # Key provided matches node key, return value
                return self.storage[hashed_key].value
            else:
                # Next pointer is another node, search for matching key in list
                if self.storage[hashed_key].next:
                    # Find matching key and return its value
                    node = self.storage[hashed_key]
                    while node:
                        if node.key == key:
                            return node.value
                        node = node.next
                else:
                    # While the hashed key matched a valid bucket, the key itself wasn't found in any key/value pair
                    return None
        else:
            # Hashed key does not map to a bucket
            return None

    def resize(self, direction=1):
        """
        Doubles/Halves the capacity of the hash table and
        rehashes all key/value pairs.
        """

        if direction == 1:
            # Increase size
            new_capacity = self.capacity * 2
        else:
            # Decrease size
            new_capacity = self.capacity // 2

        # Create temp hash table with doubled capacity
        temp_hash_table = HashTable(new_capacity)

        # Unpack existing table and re-hash + insert into new table
        for bucket in self.storage:
            if bucket:
                # Bucket has key/value pair
                if bucket.next:
                    # Bucket has more than 1 node attached
                    node = bucket

                    # traverse linked list and insert nodes into temp table
                    while node:
                        temp_hash_table.insert(node.key, node.value)
                        node = node.next
                else:
                    temp_hash_table.insert(bucket.key, bucket.value)

        # print(f"Resized table from {self.capacity} to {new_capacity}")

        # Overwrite old self.storage with self.storage from new table
        self.capacity = new_capacity
        self.storage = temp_hash_table.storage

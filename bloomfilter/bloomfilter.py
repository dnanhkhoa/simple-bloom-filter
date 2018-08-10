#!/usr/bin/python
# -*- coding: utf-8 -*-
import math
import mmh3

from bitarray import bitarray


class BloomFilter(object):
    def __init__(self, max_items, fp_prob=1e-6):
        self.__num_items = 0
        self.__max_items = max_items
        self.__fp_prob = fp_prob

        if self.__max_items:
            self.__size = math.ceil(
                -self.__max_items * math.log(self.__fp_prob) / math.log(2) ** 2
            )
            self.__num_hashes = round(self.__size * math.log(2) / self.__max_items)

            self.__array = bitarray(self.__size, endian='little')
            self.__array.setall(False)
        else:
            self.__array = bitarray(endian='little')

    @classmethod
    def load(cls, fp):
        bloom_filter = cls()
        # bf.__array = bitarray()
        # bf.__array.fromfile(fp)
        pass

    def save(self, fp):
        pass

    @property
    def size(self):
        return self.__size

    @property
    def num_hashes(self):
        return self.__num_hashes

    @property
    def max_items(self):
        return self.__max_items

    def __len__(self):
        return self.__num_items

    def add(self, item):
        if item not in self:
            for i in range(self.__num_hashes):
                self.__array[mmh3.hash(item, i) % self.__size] = True
            self.__num_items += 1

    def __contains__(self, item):
        for i in range(self.__num_hashes):
            if not self.__array[mmh3.hash(item, i) % self.__size]:
                return False
        return True


def main():
    bf = BloomFilter(10)
    pass


if __name__ == "__main__":
    main()

#!/usr/bin/python
# -*- coding: utf-8 -*-
import math
import mmh3
from enum import IntEnum
from struct import pack, unpack, calcsize

from bitarray import bitarray


class BloomFilter(object):
    def __init__(self, size, fp_prob=1e-6):
        self.__size_used = 0
        self.__size = size
        self.__fp_prob = fp_prob

        if self.__size:
            self.__filter_size = math.ceil(
                -self.__size * math.log(self.__fp_prob) / math.log(2) ** 2
            )
            self.__num_hashes = round(self.__filter_size * math.log(2) / self.__size)

            self.__filter = bitarray(self.__filter_size, endian="little")
            self.__filter.setall(False)
        else:
            self.__filter = bitarray(endian="little")

    @classmethod
    def load(cls, fp, n=-1):
        header = "<dQQQQ"
        header_size = calcsize(header)
        fp_prob, size_used, size, filter_size, num_hashes = unpack(
            header, fp.read(header_size)
        )
        bloom_filter = cls(size=0, fp_prob=fp_prob)
        if n >= header_size:
            bloom_filter.__filter.frombytes(fp.read(n - header_size))
        else:
            bloom_filter.__filter.frombytes(fp.read())
        assert bloom_filter.__filter.length() == filter_size or bloom_filter.__filter.length() == filter_size + (
                8 - filter_size % 8
        ), "Bloom filter size mismatch!"
        bloom_filter.__size_used = size_used
        bloom_filter.__size = size
        bloom_filter.__filter_size = filter_size
        bloom_filter.__num_hashes = num_hashes
        return bloom_filter

    def save(self, fp):
        fp.write(
            pack(
                "<dQQQQ",
                self.__fp_prob,
                self.__size_used,
                self.__size,
                self.__filter_size,
                self.__num_hashes,
            )
        )
        fp.write(self.__filter.tobytes())

    @property
    def filter_size(self):
        return self.__filter_size

    @property
    def num_hashes(self):
        return self.__num_hashes

    @property
    def fp_prob(self):
        return self.__fp_prob

    @property
    def size(self):
        return self.__size

    def __len__(self):
        return self.__size_used

    def add(self, item):
        if item not in self and self.__size_used < self.__size:
            for i in range(self.__num_hashes):
                self.__filter[mmh3.hash(item, i) % self.__filter_size] = True
            self.__size_used += 1

    def __contains__(self, item):
        for i in range(self.__num_hashes):
            if not self.__filter[mmh3.hash(item, i) % self.__filter_size]:
                return False
        return True


class SizeGrowthRate(IntEnum):
    SMALL = 2
    LARGE = 4


class ScalableBloomFilter(object):
    """
    References:
    + http://gsd.di.uminho.pt/members/cbm/ps/dbloom.pdf
    + https://github.com/jaybaird/python-bloomfilter
    """

    def __init__(
            self,
            initial_size=100,
            initial_fp_prob=1e-6,
            size_growth_rate=SizeGrowthRate.LARGE,
            fp_prob_rate=0.9,
    ):
        self.__initial_size = initial_size
        self.__initial_fp_prob = initial_fp_prob
        self.__size_growth_rate = size_growth_rate
        self.__fp_prob_rate = fp_prob_rate
        self.__filters = []

        if self.__initial_size:
            self.__filters.append(
                BloomFilter(size=self.__initial_size, fp_prob=self.__initial_fp_prob)
            )

    @classmethod
    def load(cls, fp):
        header = "<QdQdQ"
        initial_size, initial_fp_prob, size_growth_rate, fp_prob_rate, num_filters = unpack(
            header, fp.read(calcsize(header))
        )
        scalable_bloom_filter = cls(
            initial_size=0,
            initial_fp_prob=initial_fp_prob,
            size_growth_rate=size_growth_rate,
            fp_prob_rate=fp_prob_rate,
        )
        scalable_bloom_filter.__initial_size = initial_size
        header = "<" + "Q" * num_filters
        filter_sizes = unpack(header, fp.read(calcsize(header)))
        for filter_size in filter_sizes:
            scalable_bloom_filter.__filters.append(BloomFilter.load(fp, filter_size))
        return scalable_bloom_filter

    def save(self, fp):
        fp.write(
            pack(
                "<QdQdQ",
                self.__initial_size,
                self.__initial_fp_prob,
                self.__size_growth_rate,
                self.__fp_prob_rate,
                len(self.__filters),
            )
        )
        header_pos = fp.tell()
        header = "<" + "Q" * len(self.__filters)
        fp.write(b"\0" * calcsize(header))
        filter_sizes = []
        for bloom_filter in self.__filters:
            begin = fp.tell()
            bloom_filter.save(fp)
            filter_sizes.append(fp.tell() - begin)

        fp.seek(header_pos)
        fp.write(pack(header, *filter_sizes))

    @property
    def num_filters(self):
        return len(self.__filters)

    @property
    def filter_size(self):
        return sum(bloom_filter.filter_size for bloom_filter in self.__filters)

    @property
    def size(self):
        return sum(bloom_filter.size for bloom_filter in self.__filters)

    @property
    def fp_prob(self):
        return 1 - math.exp(
            sum(
                map(
                    lambda bloom_filter: math.log(1 - bloom_filter.fp_prob),
                    self.__filters,
                )
            )
        )

    def __len__(self):
        return sum(len(bloom_filter) for bloom_filter in self.__filters)

    def add(self, item):
        if self.__filters and item not in self:
            bloom_filter = self.__filters[-1]
            if len(bloom_filter) >= bloom_filter.size:
                bloom_filter = BloomFilter(
                    size=bloom_filter.size * self.__size_growth_rate,
                    fp_prob=bloom_filter.fp_prob * self.__fp_prob_rate,
                )
                self.__filters.append(bloom_filter)
            bloom_filter.add(item)

    def __contains__(self, item):
        for bloom_filter in reversed(self.__filters):
            if item in bloom_filter:
                return True
        return False

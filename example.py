#!/usr/bin/python
# -*- coding: utf-8 -*-
from bloomfilter import BloomFilter, ScalableBloomFilter, SizeGrowthRate

animals = [
    "dog",
    "cat",
    "giraffe",
    "fly",
    "mosquito",
    "horse",
    "eagle",
    "bird",
    "bison",
    "boar",
    "butterfly",
    "ant",
    "anaconda",
    "bear",
    "chicken",
    "dolphin",
    "donkey",
    "crow",
    "crocodile",
]

other_animals = [
    "badger",
    "cow",
    "pig",
    "sheep",
    "bee",
    "wolf",
    "fox",
    "whale",
    "shark",
    "fish",
    "turkey",
    "duck",
    "dove",
    "deer",
    "elephant",
    "frog",
    "falcon",
    "goat",
    "gorilla",
    "hawk",
]


def bloom_filter_example():
    print("========== Bloom Filter Example ==========")
    bloom_filter = BloomFilter(size=1000, fp_prob=1e-6)

    # Insert items into Bloom filter
    for animal in animals:
        bloom_filter.add(animal)

    # Print several statistics of the filter
    print(
        "+ Capacity: {} item(s)".format(bloom_filter.size),
        "+ Number of inserted items: {}".format(len(bloom_filter)),
        "+ Filter size: {} bit(s)".format(bloom_filter.filter_size),
        "+ False Positive probability: {}".format(bloom_filter.fp_prob),
        "+ Number of hash functions: {}".format(bloom_filter.num_hashes),
        sep="\n",
        end="\n\n",
    )

    # Check whether an item is in the filter or not
    for animal in animals + other_animals:
        if animal in bloom_filter:
            if animal in other_animals:
                print(
                    f'"{animal}" is a FALSE POSITIVE case (please adjust fp_prob to a smaller value).'
                )
            else:
                print(f'"{animal}" is PROBABLY IN bloom filter.')
        else:
            print(f'"{animal}" is DEFINITELY NOT in bloom filter as expected.')

    # Save to file
    with open("bloom_filter.bin", "wb") as fp:
        bloom_filter.save(fp)

    # Load from file
    with open("bloom_filter.bin", "rb") as fp:
        bloom_filter = BloomFilter.load(fp)


def scalable_bloom_filter_example():
    print("========== Bloom Filter Example ==========")
    scalable_bloom_filter = ScalableBloomFilter(
        initial_size=100,
        initial_fp_prob=1e-7,
        size_growth_rate=SizeGrowthRate.LARGE,
        fp_prob_rate=0.9,
    )
    # Insert items into Bloom filter
    for animal in animals:
        scalable_bloom_filter.add(animal)

    # Print several statistics of the filter
    print(
        "+ Capacity: {} item(s)".format(scalable_bloom_filter.size),
        "+ Number of inserted items: {}".format(len(scalable_bloom_filter)),
        "+ Number of Bloom filters: {}".format(scalable_bloom_filter.num_filters),
        "+ Total size of filters: {} bit(s)".format(scalable_bloom_filter.filter_size),
        "+ False Positive probability: {}".format(scalable_bloom_filter.fp_prob),
        sep="\n",
        end="\n\n",
    )

    # Check whether an item is in the filter or not
    for animal in animals + other_animals:
        if animal in scalable_bloom_filter:
            if animal in other_animals:
                print(
                    f'"{animal}" is a FALSE POSITIVE case (please adjust fp_prob to a smaller value).'
                )
            else:
                print(f'"{animal}" is PROBABLY IN bloom filter.')
        else:
            print(f'"{animal}" is DEFINITELY NOT in bloom filter as expected.')

    # Save to file
    with open("scalable_bloom_filter.bin", "wb") as fp:
        scalable_bloom_filter.save(fp)

    # Load from file
    with open("scalable_bloom_filter.bin", "rb") as fp:
        scalable_bloom_filter = ScalableBloomFilter.load(fp)


if __name__ == "__main__":
    bloom_filter_example()
    scalable_bloom_filter_example()

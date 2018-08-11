# simple-bloom-filter

[![PyPI](https://img.shields.io/pypi/v/simplebloomfilter.svg)]()
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/simplebloomfilter.svg)]()

A simple implementation of Bloom Filter and Scalable Bloom Filter for Python 3.

## Installation

You can install this package from PyPI using [pip](http://www.pip-installer.org):

```
$ [sudo] pip install simplebloomfilter
```

## Example Usage

```python
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
                print(f'"{animal}" is PROBABLY IN the filter.')
        else:
            print(f'"{animal}" is DEFINITELY NOT IN the filter as expected.')

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
                print(f'"{animal}" is PROBABLY IN the filter.')
        else:
            print(f'"{animal}" is DEFINITELY NOT IN the filter as expected.')

    # Save to file
    with open("scalable_bloom_filter.bin", "wb") as fp:
        scalable_bloom_filter.save(fp)

    # Load from file
    with open("scalable_bloom_filter.bin", "rb") as fp:
        scalable_bloom_filter = ScalableBloomFilter.load(fp)


if __name__ == "__main__":
    bloom_filter_example()
    scalable_bloom_filter_example()
```

```
========== Bloom Filter Example ==========
+ Capacity: 1000 item(s)
+ Number of inserted items: 19
+ Filter size: 28756 bit(s)
+ False Positive probability: 1e-06
+ Number of hash functions: 20

"dog" is PROBABLY IN the filter.
"cat" is PROBABLY IN the filter.
"giraffe" is PROBABLY IN the filter.
"fly" is PROBABLY IN the filter.
"mosquito" is PROBABLY IN the filter.
"horse" is PROBABLY IN the filter.
"eagle" is PROBABLY IN the filter.
"bird" is PROBABLY IN the filter.
"bison" is PROBABLY IN the filter.
"boar" is PROBABLY IN the filter.
"butterfly" is PROBABLY IN the filter.
"ant" is PROBABLY IN the filter.
"anaconda" is PROBABLY IN the filter.
"bear" is PROBABLY IN the filter.
"chicken" is PROBABLY IN the filter.
"dolphin" is PROBABLY IN the filter.
"donkey" is PROBABLY IN the filter.
"crow" is PROBABLY IN the filter.
"crocodile" is PROBABLY IN the filter.
"badger" is DEFINITELY NOT IN the filter as expected.
"cow" is DEFINITELY NOT IN the filter as expected.
"pig" is DEFINITELY NOT IN the filter as expected.
"sheep" is DEFINITELY NOT IN the filter as expected.
"bee" is DEFINITELY NOT IN the filter as expected.
"wolf" is DEFINITELY NOT IN the filter as expected.
"fox" is DEFINITELY NOT IN the filter as expected.
"whale" is DEFINITELY NOT IN the filter as expected.
"shark" is DEFINITELY NOT IN the filter as expected.
"fish" is DEFINITELY NOT IN the filter as expected.
"turkey" is DEFINITELY NOT IN the filter as expected.
"duck" is DEFINITELY NOT IN the filter as expected.
"dove" is DEFINITELY NOT IN the filter as expected.
"deer" is DEFINITELY NOT IN the filter as expected.
"elephant" is DEFINITELY NOT IN the filter as expected.
"frog" is DEFINITELY NOT IN the filter as expected.
"falcon" is DEFINITELY NOT IN the filter as expected.
"goat" is DEFINITELY NOT IN the filter as expected.
"gorilla" is DEFINITELY NOT IN the filter as expected.
"hawk" is DEFINITELY NOT IN the filter as expected.


========== Bloom Filter Example ==========
+ Capacity: 100 item(s)
+ Number of inserted items: 19
+ Number of Bloom filters: 1
+ Total size of filters: 3355 bit(s)
+ False Positive probability: 9.999999994736442e-08

"dog" is PROBABLY IN the filter.
"cat" is PROBABLY IN the filter.
"giraffe" is PROBABLY IN the filter.
"fly" is PROBABLY IN the filter.
"mosquito" is PROBABLY IN the filter.
"horse" is PROBABLY IN the filter.
"eagle" is PROBABLY IN the filter.
"bird" is PROBABLY IN the filter.
"bison" is PROBABLY IN the filter.
"boar" is PROBABLY IN the filter.
"butterfly" is PROBABLY IN the filter.
"ant" is PROBABLY IN the filter.
"anaconda" is PROBABLY IN the filter.
"bear" is PROBABLY IN the filter.
"chicken" is PROBABLY IN the filter.
"dolphin" is PROBABLY IN the filter.
"donkey" is PROBABLY IN the filter.
"crow" is PROBABLY IN the filter.
"crocodile" is PROBABLY IN the filter.
"badger" is DEFINITELY NOT IN the filter as expected.
"cow" is DEFINITELY NOT IN the filter as expected.
"pig" is DEFINITELY NOT IN the filter as expected.
"sheep" is DEFINITELY NOT IN the filter as expected.
"bee" is DEFINITELY NOT IN the filter as expected.
"wolf" is DEFINITELY NOT IN the filter as expected.
"fox" is DEFINITELY NOT IN the filter as expected.
"whale" is DEFINITELY NOT IN the filter as expected.
"shark" is DEFINITELY NOT IN the filter as expected.
"fish" is DEFINITELY NOT IN the filter as expected.
"turkey" is DEFINITELY NOT IN the filter as expected.
"duck" is DEFINITELY NOT IN the filter as expected.
"dove" is DEFINITELY NOT IN the filter as expected.
"deer" is DEFINITELY NOT IN the filter as expected.
"elephant" is DEFINITELY NOT IN the filter as expected.
"frog" is DEFINITELY NOT IN the filter as expected.
"falcon" is DEFINITELY NOT IN the filter as expected.
"goat" is DEFINITELY NOT IN the filter as expected.
"gorilla" is DEFINITELY NOT IN the filter as expected.
"hawk" is DEFINITELY NOT IN the filter as expected.
```

## License

MIT

#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

from setuptools import setup


def readme(file_name):
    if os.path.isfile(file_name):
        with open(file_name, 'r', encoding='UTF-8') as f:
            return f.read()


setup(name='simplebloomfilter',
      version='1.0.0',
      description='A simple implementation of Bloom Filter and Scalable Bloom Filter for Python 3.',
      long_description=readme(file_name='README.md'),
      keywords='bloom-filter scalable-bloom-filter bloomfilter python-3 hashing algorithm data-structure',
      url='https://github.com/dnanhkhoa/simple-bloom-filter',
      author='Khoa Duong',
      author_email='dnanhkhoa@live.com',
      license='MIT',
      packages=['bloomfilter'],
      zip_safe=False,
      install_requires=['mmh3', 'bitarray'],
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3'
      ])

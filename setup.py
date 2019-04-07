#!/usr/bin/env python
# -*- coding: utf-8 -*-
import setuptools

import binary_search_tree as bst

__version__ = bst.__version__
__author__ = bst.__author__
__email__ = bst.__email__


with open("requirements.txt") as f:
    requirements = list(f.readlines())

with open("requirements_setup.txt") as f:
    setup_requirements = list(f.readlines())

with open("requirements_test.txt") as f:
    test_requirements = list(f.readlines())


setuptools.setup(
    name="binary_search_tree",
    version=__version__,
    author=__author__,
    author_email=__email__,
    packages=setuptools.find_packages(),
    install_requires=requirements,
    setup_requires=setup_requirements,
    test_requires=test_requirements,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: Freely Distributable",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries"
    ]
)

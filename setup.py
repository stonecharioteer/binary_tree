#!/usr/bin/env python
# -*- coding: utf-8 -*-
import setuptools
import binary_tree as bt

__version__ = bt.__version__
__author__ = bt.__author__
__email__ = bt.__email__


with open("requirements.txt") as f:
    requirements = list(f.readlines())

with open("requirements_setup.txt") as f:
    setup_requirements = list(f.readlines())

with open("requirements_test.txt") as f:
    test_requirements = list(f.readlines())


setuptools.setup(
    name="binary_tree",
    version=__version__,
    author=__author__,
    author_email=__email__,
    packages=setuptools.find_packages(),
    install_requires=requirements,
    setup_requires=setup_requirements,
    tests_require=test_requirements,
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

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pickle
import pytest
import binary_search_tree as bst


@pytest.fixture(scope="module")
def sample_bst():
    import random
    sample_data = set([random.randint(0,100000) for i in range(5000)])
    sample_tree = bst.BinarySearchTree()
    for ix, i in enumerate(sample_data):
        sample_tree[ix] = i
    yield sample_tree
    del sample_tree


def test_tree(sample_bst):
    """Test that a simple bst can be constructed with the code."""
    assert isinstance(sample_bst, bst.BinarySearchTree)
    print(sample_bst)
    print(len(sample_bst))
    assert False


def test_tree_pickle(sample_bst):
    """Test that a simple bst can be constructed with the code."""
    test_file = os.path.join(os.getcwd(),"sample_bst.dat")
    if os.path.exists(test_file):
        os.remove(test_file)
    sample_bst.dump(test_file)
    sample_bst_2 = bst.load(test_file)
    assert isinstance(sample_bst_2, bst.BinarySearchTree)
    assert len(sample_bst) == len(sample_bst_2)
    for i, j in zip(sample_bst, sample_bst_2):
        assert i == j
        assert sample_bst[i] == sample_bst_2[j]

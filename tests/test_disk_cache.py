#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pickle
import pytest
import binary_search_tree as bst


@pytest.fixture
def sample_bst():
    import random
    sample_data = set([random.randint(0,100000) for i in range(100)])
    sample_tree = bst.BinarySearchTree(cache="sample.db")
    for ix, i in enumerate(sample_data):
        sample_tree[ix] = i
    yield sample_tree
    del sample_tree
    os.remove("sample.db")


def test_tree(sample_bst):
    """Test that a simple bst can be constructed with the code."""
    assert isinstance(sample_bst, bst.BinarySearchTree)


@pytest.fixture
def sample_bst_cache():
    import random
    sample_data = set(["payload_{}".format(i) for i in range(300)])
    sample_tree = bst.BinarySearchTree(cache="sample.db")
    for ix, i in enumerate(sample_data):
        sample_tree[ix] = i
    yield sample_tree, "sample.db"
    os.remove("sample.db")

def test_tree_cache(sample_bst_cache):
    """Tests that a prior cached tree can be read from."""
    import shutil
    import sys
    sys.setrecursionlimit(5000) # bypass Python's recursion limit for the sake of
    # this exercise
    cached_bst, cache_file = sample_bst_cache
    shutil.copy2(cache_file, "sample_2.db")
    loaded_bst = bst.BinarySearchTree("sample_2.db")
    assert isinstance(loaded_bst, bst.BinarySearchTree)
    for key in loaded_bst:
        assert key in cached_bst, (
            "Node in the previously generated tree does "
            "not exist in the loaded tree")
        assert cached_bst[key] == loaded_bst[key], (
            "Node in the previously generated tree doesn't have "
            "the same payload in the loaded tree")

    os.remove("sample_2.db")

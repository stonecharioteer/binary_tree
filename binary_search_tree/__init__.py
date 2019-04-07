#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Binary Search Tree module.

This library allows creation of Binary Search Trees. These trees can grow to
be any size. The tree items are cached on disk, and read from disk on demand.


"""
__all__ = ["BinarySearchTree", "TreeNode"]
__version__ = "2019.04-alpha"
__author__ = "Vinay Keerthi"
__email__ = "ktvkvinaykeerthi+binary_search_tree@gmail.com"

from binary_search_tree.binary_search_tree import BinarySearchTree
from binary_search_tree.tree_node import TreeNode

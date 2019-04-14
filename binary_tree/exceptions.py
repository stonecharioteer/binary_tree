#!/usr/bin/env python
# -*- coding: utf-8 -*-


class InvalidTraversalMode(Exception):
    """Exception raised when the mode isn't acceptable, or
    it isn't anticipated. Right now, the only implemented
    modes are inorder, postorder and preorder."""
    pass


class InsufficientTraversalInformation(Exception):
    """Exception raised when not enough traversal caches
    are specified to the load method of the TreeNode class.
    At least 2 of the 3 types are required at any point of time."""
    pass

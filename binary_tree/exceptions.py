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


class InvalidValueError(Exception):
    """Exception raised when a noninteger value is passed to the initializer
    of the TreeNode class.
    Note: caveat: There is currently no check in place if a user manually
    accesses the value and overwrites it.
    That is apt for a later adaptation."""
    pass


class InvalidChildError(Exception):
    """Exception raised when a non TreeNode object is assigned to the left
    or right child of the initializer of the TreeNode class.
    Note: caveat: There is currently no check in place if a user
    manually accesses the left or right child values and overwrites them.
    That is apt for a later adaptation.
    """
    pass

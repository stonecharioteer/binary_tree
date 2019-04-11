#!/usr/bin/env python
# -*- coding: utf-8 -*-
import shelve

class TreeNode:
    """Class definition for each node."""
    def __init__(
        self, key, value,
        left=None, right=None, parent=None):
        """Initializer method."""
        self.key = key
        self.payload = value
        self.left_child = left
        self.right_child = right
        self.parent = parent

    def __repr__(self):
        repr_node = "<TreeNode [Key: {}, payload: {}]>".format(
            self.key, self.payload)
        return repr_node

    def __iter__(self):
        if self:
            if self.has_left_child():
                for element in self.left_child:
                    yield element
            yield self.key
            if self.has_right_child():
                for element in self.right_child:
                    yield element

    @property
    def position(self):
        if self.is_leaf():
            if self.is_left_child():
                return "left leaf"
            if self.is_right_child():
                return "right leaf"
        else:
            if self.is_left_child():
                return "left child"
            if self.is_right_child():
                return "right child"

    def has_left_child(self):
        """Check if this node has a left child."""
        return self.left_child is not None

    def has_right_child(self):
        """Check if this node has a right child."""
        return self.right_child is not None

    def has_both_children(self):
        return self.has_left_child() and self.has_right_child()

    def is_root(self):
        """Check if this node is a root node."""
        return self.parent is None

    def is_left_child(self):
        """Check if this node is a left child."""
        return (not self.is_root()) and (self.parent.left_child == self)

    def is_right_child(self):
        """Check if this node is a right child."""
        return (not self.is_root()) and (self.parent.right_child == self)

    def is_leaf(self):
        """Checks if this node is a leaf, ie. it does not have children."""
        return not (self.has_left_child() or self.has_right_child())

    def has_children(self):
        """Checks if this node has children."""
        return not self.is_leaf()

    def replace_node_data(self, key, value, left_child, right_child):
        self.key=key
        self.payload = value
        self.left_child = left_child
        self.right_child = right_child
        if self.has_left_child():
            self.left_child.parent = self
        if self.has_right_child():
            self.right_child.parent = self

    def __eq__(self, other):
        return self.payload == other.payload

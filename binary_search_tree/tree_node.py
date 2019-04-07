#!/usr/bin/env python
# -*- coding: utf-8 -*-


class TreeNode:
    def __init__(self, key, value, left=None, right=None, parent=None):
        self.key = key
        self.value = value
        self.left_child = left
        self.right_child = right
        self.parent = parent


    def has_left_child(self):
        return self.left_child is not None

    def has_right_child(self):
        return self.right_child is not None

    def is_left_child(self):
        return (self.parent is not None) and (self.parent.left_child == self)

    def is_right_child(self):
        return (self.parent is not None) and (self.parent.right_child == self)

    def is_root(self):
        return self.parent is None

    def is_leaf(self):
        return (self.left_child is None) and (self.right_child is None)

    def has_children(self):
        return (self.left_child is not None) or (self.right_child is not None)

    def has_both_children(self):
        return (self.left_child is not None) and (self.right_child is not None)

    def replace_node_data(self, key, value, left_child, right_child):
        self.key=key
        self.payload = value
        self.left_child = left_child
        self.right_child = right_child
        if self.has_left_child():
            self.left_child.parent = self
        if self.has_right_child():
            self.right_child.parent = self

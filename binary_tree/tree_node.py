#!/usr/bin/env python
# -*- coding: utf-8 -*-
from binary_tree.exceptions import InvalidTraversalMode

class TreeNode:
    """Class definition for each node of a binary tree."""

    def __init__(
        self, value,
        left=None, right=None, parent=None):
        """Initializer method."""
        self.value = value
        self.left_child = left
        self.right_child = right
        self.parent = parent

    def __repr__(self):
        repr_node = "<TreeNode [Value: {}]>".format(self.value)
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

    def __eq__(self, other):
        return self.value == other.value

    @staticmethod
    def traverse(node, mode="preorder"):
        """returns the tree traversal given a node in one of 3 modes.
        The accepted values for mode are: preorder, postorder or inorder.
        """
        if mode.lower() == "preorder":
            traversal = [node.value]
            if node.left_child:
                traversal.extend(
                    TreeNode.traverse(node.left_child, mode=mode))
            if node.right_child:
                traversal.extend(
                    TreeNode.traverse(node.right_child, mode=mode))
        elif mode.lower() == "postorder":
            traversal = []
            if node.left_child:
                traversal.extend(
                    TreeNode.traverse(node.left_child, mode=mode))
            if node.right_child:
                traversal.extend(
                    TreeNode.traverse(node.right_child, mode=mode))
            traversal.append(node.value)
        elif mode.lower() == "inorder":
            traversal = []
            if node.left_child:
                traversal.extend(
                    TreeNode.traverse(node.left_child, mode=mode))
            traversal.append(node.value)
            if node.right_child:
                traversal.extend(
                    TreeNode.traverse(node.right_child, mode=mode))
        else:
            raise InvalidTraversalMode(
            ("{} is not an acceptable or "
            "implemented form of traversal! "
            "Choose from preorder, postorder "
            "or inorder traversal.").format(mode))
        return traversal

    def save_to_disk(
        file_prefix, preorder=True, inorder=True, postorder=False):
        """Saves a node and its children into 2 files.
        To check for a unique tree, you need one of two traversal information
        if the tree is not balanced or sorted.
        """

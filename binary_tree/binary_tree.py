#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import shelve
import tempfile


from binary_tree.tree_node import TreeNode
from binary_tree.tail_call_optimized import tail_call_optimized

class BinaryTree:
    """Base definition for a serializable BinaryTree."""
    def __init__(self, cache):
        """Initialization method. Pass a valid file path to the cache
        argument. This creates a shelve file, which utilizes a serialized
        store of the tree and its values."""
        self.root = None
        self.size = 0
        self.cache = shelve.open(cache, writeback=True)
        for key in self.cache:
            self[int(key)] = self.cache[key].payload

    def __repr__(self):
        return "<BinarySearchTree [Size: {}, root: {}]>".format(
            self.size, self.root)

    def __len__(self):
        """Length method."""
        return self.size

    def length(self):
        """Internal length method."""
        return self.__len__()

    def __iter__(self):
        """Enables behaviour as an iterator."""
        return self.root.__iter__()

    #@tail_call_optimized
    def put(self, key, value):
        """Internal helper method that interfaces with __setitem___"""
        if self.root is not None:
            try:
                self._put(key, value, self.root)
            except RecursionError as e:
                import sys
                rec_limit = sys.getrecursionlimit()
                raise RecursionError(
                        "Python's interpreter limits the "
                        "maximum recursion limit to ~{} on this machine. "
                        "This is done to guard against stack overflow "
                        "because the CPython implementation doesn't "
                        "optimize tail recursion, and unbridled recursions "
                        "can trigger stack overflows. This creates problems "
                        "with very large binary trees, "
                        "Increase the limit as you require. "
                        "It is usually 3x the "
                        "size of the tree.".format(rec_limit))
        else:
            if self.cache.get(str(key)):
                self.root = self.cache.get(str(key))
            else:
                self.cache[str(key)] = TreeNode(key, value)
                self.root = self.cache[str(key)]

        self.size += 1

    @tail_call_optimized
    def _put(self, key, value, current_node):
        """Internal method to interfere when attempting to put a value into an
        empty node."""
        if key < current_node.key:
            if current_node.has_left_child():
                self._put(key, value, current_node.left_child)
            else:
                # Refresh the current node
                self.cache[str(key)] = TreeNode(
                    key, value, parent=current_node)
                self.cache[str(current_node.key)] = TreeNode(
                    current_node.key,
                    current_node.payload,
                    parent=current_node.parent,
                    left=self.cache[str(key)]
                    )
                # FIXME: Is this part necessary now?
                current_node.left_child = self.cache[str(key)]
        else:
            if current_node.has_right_child():
                self._put(key, value, current_node.right_child)
            else:
                self.cache[str(key)] = TreeNode(
                    key, value, parent=current_node)
                # Refresh the current node
                self.cache[str(current_node.key)] = TreeNode(
                    current_node.key,
                    current_node.payload,
                    parent=current_node.parent,
                    right=self.cache[str(key)]
                    )
                current_node.right_child = self.cache[str(key)]

    def __setitem__(self, key, value):
        """Method to enable the indexing behaviour."""
        self.put(key, value)

    def get(self, key):
        """Internal method to get a value given the key.
        Interacts with __getitem__"""
        if self.root:
            res = self._get(key, self.root)
            if res:
                return res.payload
            else:
                return None
        else:
            return None

    def _get(self, key, current_node):
        """Internal method that interferes when there is no root in
        this node."""
        # FIXME: Where do I put the cache retrieval?
        if current_node is None:
            return None
        elif current_node.key == key:
            return self.cache[str(key)]
            # return current_node
        elif key < current_node.key:
            return self._get(key, current_node.left_child)
        else:
            return self._get(key, current_node.right_child)

    def __getitem__(self, key):
        """Method to enable the indexing behaviour and its retrieval."""
        return self.get(key)

    def __contains__(self, key):
        """Method to enable usage of the in keyword."""
        if self._get(key, self.root):
            return True
        else:
            return False

    def delete(self, key):
        """Deletes a node from the tree."""
        if self.size > 1:
            node_to_remove = self._get(key, self.root)
            if node_to_remove is not None:
                self.remove(node_to_remove)
                self.size -= 1
            else:
                raise KeyError("Error, key ({}) not in tree!".format(key))
        elif self.size == 1 and self.root.key == key:
            self.root = None
            self.size -= 1
        else:
            raise KeyError("Error, key ({}) not in tree!".format(key))

    def __delitem__(self, key):
        """Enables deletion of a key."""
        self.delete(key)

    def remove(self, current_node):
        """Method to remove a node from the tree and promote children
        in its place."""
        if current_node.is_leaf():
            if current_node.is_left_child():
                current_node.parent.left_child = None
            else:
                current_node.parent.right_child = None
        elif current_node.has_both_children():
            successor = current_node.find_successor()
            successor.splice_out()
            current_node.key = successor.key
            current_node.payload = successor.payload
        else:
            if current_node.has_left_child():
                if current_node.is_left_child():
                    current_node.left_child.parent = current_node.parent
                    current_node.parent.left_child = current_node.left_child
                elif current_node.is_right_child():
                    current_node.left_child.parent = current_node.parent
                    current_node.parent.right_child = current_node.left_child
                else:
                    current_node.replace_node_data(
                        current_node.left_child.key,
                        current_node.left_child.payload,
                        current_node.left_child.left_child,
                        current_node.left_child.left_child,
                        current_node.left_child.right_child)
            else:
                if current_node.is_left_child():
                    current_node.right_child.parent = current_node.parent
                    current_node.parent.left_child = current_node.right_child
                elif current_node.is_right_child():
                    current_node.right_child.parent = current_node.parent
                    current_node.parent.right_child = current_node.right_child
                else:
                    current_node.replace_node_data(
                        current_node.right_child.key,
                        current_node.right_child.payload,
                        current_node.right_child.left_child,
                        current_node.right_child.left_child,
                        current_node.right_child.right_child)

    def find_successor(self):
        """Method to find the successor node, which is used after deletion
        of a node from the tree."""
        successor = None
        if self.has_right_child():
            successor = self.right_child.find_min()
        else:
            if self.parent:
                if self.is_left_child():
                    successor = self.parent
                else:
                    self.parent.right_child = None
                    successor = self.parent.find_successor()
                    self.parent.right_child = self
        return successor

    def find_min(self):
        """Finds the smallest value of a subtree."""
        current = self
        while current.has_left_child():
            current = current.left_child
        return current

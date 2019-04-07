#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import tempfile


from binary_search_tree.tree_node import TreeNode
from binary_search_tree.tail_call_optimized import tail_call_optimized

class BinarySearchTree:
    """Base definition for a serializable BinarySearchTree."""
    def __init__(self, cache=None):
        """Initialization method. Pass a valid file path to the cache
        argument. Leave it out if you're okay with the code creating a
        tempfile which will be garbage collected later."""
        # if cache is None:
        #     self.cache = tempfile.TemporaryFile()
        # else:
        #     self.cache = cache
        self.root = None
        self.size = 0

    def __repr__(self):
        return "<BinarySearchTree [Size: {}, root: {}]>".format(
            self.size, self.root)

    @tail_call_optimized
    def dump(self, file_path):
        """Method to serialize and dump to a file.
        This method dumps the entire tree into a file."""
        import pickle
        with open(file_path, "w") as f:
            pickle.dump(self, f)

    @staticmethod
    def load(cls, file_path):
        """Method to unserialize and load from a previously dumped file.
        This method loads an entire tree into memory."""
        import pickle
        with open(file_path, "r") as f:
            return pickle.load(f)

    def __len__(self):
        """Length method."""
        return self.size

    def length(self):
        """Internal length method."""
        return self.__len__()

    @tail_call_optimized
    def __iter__(self):
        """Enables behaviour as an iterator."""
        return self.root.__iter__()

    def put(self, key, value):
        """Internal helper method that interfaces with __setitem___"""
        if self.root is not None:
            try:
                self._put(key, value, self.root)
            except RecursionError as e:
                import sys
                rec_limit = sys.getrecursionlimit()
                raise RecursionError(
                    ("Python's interpreter limits the "
                "maximum recursion limit to ~{} on this machine. This is "
                "done to guard against stack overflow because the CPython "
                "implementation doesn't optimize tail recursion, and "
                "unbridled recursions can trigger stack overflows. "
                "This creates problems with very large binary search trees, "
                "Increase the limit as you require. It is usually 3x the "
                "size of the tree.").format(rec_limit))
        else:
            self.root = TreeNode(key, value)
        self.size += 1

    @tail_call_optimized
    def _put(self, key, value, current_node):
        """Internal method to interfere when attempting to put a value into an
        empty node."""
        if key < current_node.key:
            if current_node.has_left_child():
                self._put(key, value, current_node.left_child)
            else:
                current_node.left_child = TreeNode(
                    key, value, parent=current_node)
        else:
            if current_node.has_right_child():
                self._put(key, value, current_node.right_child)
            else:
                current_node.right_child = TreeNode(
                    key, value, parent=current_node)

    def __setitem__(self, key, value):
        """Method to enable the indexing behaviour."""
        self.put(key, value)

    def get(self, key):
        """Internal method to get a value given the key.
        Interacts with __getitem__"""
        if self.root is not None:
            res = self._get(key, self.root)
            if res:
                return res.payload
            else:
                return None
        else:
            return None

    @tail_call_optimized
    def _get(self, key, current_node):
        """Internal method that interferes when there is no root in
        this node."""
        if current_node is None:
            return None
        elif current_node.key == key:
            return current_node
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

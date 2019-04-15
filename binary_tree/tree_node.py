#!/usr/bin/env python
# -*- coding: utf-8 -*-
from binary_tree.exceptions import (
    InvalidTraversalMode, InsufficientTraversalInformation,
    InvalidChildError, InvalidValueError)

class TreeNode:
    """Class definition for each node of a binary tree."""

    def __init__(self, value, left=None, right=None):
        """Initializer method.
        Takes an integer value, a left node and a right node."""
        if not isinstance(value, int):
            raise InvalidValueError(
                "Since this tree is created for the sake of demonstrating "
                "how such a tree could be serialized, the author has "
                "limited creation to trees wherein the value "
                "must be integers.")
        self.value = value
        if left is not None:
            if not isinstance(left, TreeNode):
                raise InvalidChildError("Nodes must of type TreeNode!")
        self.left_child = left
        if right is not None:
            if not isinstance(right, TreeNode):
                raise InvalidChildError("Nodes must of type TreeNode!")
        self.right_child = right

    def __repr__(self):
        """Raw Representation."""
        repr_node = "<TreeNode [Value: {}] [L: {} | R: {}]>".format(
            self.value,
            self.left_child.value if self.left_child else "-",
            self.right_child.value if self.right_child else "-")
        return repr_node

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
        self, file_prefix, preorder=True, inorder=True, postorder=False):
        """Saves a node and its children into 2 files.
        To check for a unique tree, you need one of two traversal information
        if the tree is not balanced or sorted.
        """
        if inorder:
            inorder = TreeNode.traverse(self, mode="inorder")
            with open("{}.inorder".format(file_prefix), "wb+") as f:
                for node in inorder:
                    f.write("{}\n".format(node).encode("utf-8"))
        if preorder:
            preorder = TreeNode.traverse(self, mode="preorder")
            with open("{}.preorder".format(file_prefix), "wb+") as f:
                for node in preorder:
                    f.write("{}\n".format(node).encode("utf-8"))
        if postorder:
            postorder = TreeNode.traverse(self, mode="postorder")
            with open("{}.postorder".format(file_prefix), "wb+") as f:
                for node in postorder:
                    f.write("{}\n".format(node).encode("utf-8"))

    @staticmethod
    def load(preorder=None, postorder=None, inorder=None):
        """Loads the binary tree given two of these three traversals.
        If given preorder and inorder, it uses that.

        """
        data_is_sufficient = (preorder and inorder) or (
            postorder and inorder) or (preorder and postorder)
        if not data_is_sufficient:
            raise InsufficientTraversalInformation(
                "Specify at least 2 of the three modes to load a "
                "unique Binary Tree.")
        if preorder and inorder:
            # Pick the first item of the preorder. This is the root node.
            root = preorder[0]
            # Create a node with that root.
            node = TreeNode(root)
            # identify the new preorder. This is the preorder without the root.
            new_preorder = preorder[1:]
            # Now, identify which is the left child of this node.
            # This information is in the inorder traversal.
            # Get all the nodes left of this root using the inorder traversal.

            if root in inorder:  # if the root is in the inorder traversal.
                # find where it occurs.

                root_position = inorder.index(root)
                # split the inorder traversal list at that index.
                left_inorder = inorder[:root_position]

                if len(left_inorder) > 0:
                    # filter the preorder so that it only contains items
                    # in the left inorder traversal list.
                    left_preorder = [
                        n for n in new_preorder if n in left_inorder]
                    node.left_child = TreeNode.load(
                        preorder=left_preorder,
                        inorder=left_inorder)
                # if the root occurs before the end of the preorder.
                if root_position < len(preorder):
                    # split the inorder traversal tree at the root.
                    # Take the right half
                    right_inorder = inorder[root_position + 1:]
                    # if there *is* a right traversal tree.
                    if len(right_inorder) > 0:
                        # filter the preorder so that it only contains items
                        # in the right inorder traversal list.
                        right_preorder = [
                            n for n in new_preorder if n in right_inorder]
                        node.right_child = TreeNode.load(
                            preorder=right_preorder, inorder=right_inorder)
            return node
        elif postorder and inorder:
            # If the postorder and inorder traversal information is provided.
            node = None
            return node
        else:  # there's only one case remaining.
            # if preorder and postorder are specified.
            # This is the last possible combination.
            node = None
            return node

    @staticmethod
    def parse_files(preorder=None, postorder=None, inorder=None):
        """Parses files and loads the tree from them."""
        data_is_sufficient = (preorder and inorder) or (
            postorder and inorder) or (preorder and postorder)
        if not data_is_sufficient:
            raise InsufficientTraversalInformation(
                "Specify at least 2 of the three modes to load a "
                "unique Binary Tree")
        if preorder:
            with open(preorder, "rb+") as f:
                preorder_traversal = [
                    int(l.decode("ascii").strip()) for l in f.readlines()
                    ]

        if inorder:
            with open(inorder, "rb+") as f:
                inorder_traversal = [
                    int(l.decode("ascii").strip()) for l in f.readlines()
                    ]

        if postorder:
            with open(postorder, "rb+") as f:
                postorder_traversal = [
                    int(l.decode("ascii").strip()) for l in f.readlines()
                    ]
        if preorder and inorder:
            return TreeNode.load(
                preorder=preorder_traversal,
                inorder=inorder_traversal)
        elif postorder and inorder:
            return TreeNode.load(
                postorder=postorder_traversal,
                inorder=inorder_traversal)
        elif postorder and preorder:
            return TreeNode.load(
                postorder=postorder_traversal,
                preorder=preorder_traversal)

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from binary_tree import TreeNode


@pytest.fixture
def basic_tree():
    """Returns a basic tree with
        a preorder traversal of:
            [1, 2, 4, 5, 3]
        an inorder traversal of:
            [4, 2, 5, 1, 3]
        and a postorder traversal of:
            [4, 5, 2, 3, 1]

    """
    root = TreeNode(1)
    root.left_child = TreeNode(2)
    root.left_child.left_child = TreeNode(4)
    root.left_child.right_child = TreeNode(5)
    root.right_child = TreeNode(3)
    yield root
    del root


def test_basic_serialize_preorder(basic_tree):
    """Tests the serialization of the basic tree with preorder."""
    serialized_tree = TreeNode.traverse(basic_tree, mode="preorder")
    assert serialized_tree == [1, 2, 4, 5, 3]


def test_basic_serialize_inorder(basic_tree):
    """Tests the serialization of the basic tree with inorder traversal."""
    serialized_tree = TreeNode.traverse(basic_tree, mode="inorder")
    assert serialized_tree == [4, 2, 5, 1, 3]


def test_basic_serialize_postorder(basic_tree):
    """Tests the serialization of the basic tree with postorder traversal."""
    serialized_tree = TreeNode.traverse(basic_tree, mode="postorder")
    assert serialized_tree == [4, 5, 2, 3, 1]


def test_basic_deserialize_preorder_inorder(basic_tree):
    """Writes the tree into two files and checks if they can be read back to
    create the same tree."""
    basic_tree.save_to_disk("basic_tree")

    deserialized_tree = TreeNode.parse_files(
        preorder="basic_tree.preorder",
        inorder="basic_tree.inorder")

    assert TreeNode.traverse(
        basic_tree, mode="preorder") == TreeNode.traverse(
            deserialized_tree, mode="preorder")

    assert TreeNode.traverse(
        basic_tree, mode="postorder") == TreeNode.traverse(
            deserialized_tree, mode="postorder")

    assert TreeNode.traverse(
        basic_tree, mode="inorder") == TreeNode.traverse(
            deserialized_tree, mode="inorder")


@pytest.fixture
def longer_tree():
    """Returns a longer tree with a preorder traversal of:
        [25, 15, 10, 4, 12, 22, 18, 24, 50, 35, 31, 44, 70, 66, 90]
    """
    root = TreeNode(25)

    root.left_child = TreeNode(15)

    root.left_child.left_child = TreeNode(10)

    root.left_child.left_child.left_child = TreeNode(4)
    root.left_child.left_child.right_child = TreeNode(12)

    root.left_child.right_child = TreeNode(22)

    root.left_child.right_child.left_child = TreeNode(18)
    root.left_child.right_child.right_child = TreeNode(24)

    root.right_child = TreeNode(50)

    root.right_child.left_child = TreeNode(35)

    root.right_child.left_child.left_child = TreeNode(31)
    root.right_child.left_child.right_child = TreeNode(44)

    root.right_child.right_child = TreeNode(70)

    root.right_child.right_child.left_child = TreeNode(66)
    root.right_child.right_child.right_child = TreeNode(90)
    yield root
    del root


def test_longer_serialize_preorder(longer_tree):
    """Tests the serialization of the longer tree with preorder."""
    serialized_tree = TreeNode.traverse(longer_tree, mode="preorder")
    assert serialized_tree == [
        25, 15, 10, 4, 12, 22, 18, 24, 50, 35, 31, 44, 70, 66, 90]


def test_longer_serialize_inorder(longer_tree):
    """Tests the serialization of the longer tree with inorder traversal."""
    serialized_tree = TreeNode.traverse(longer_tree, mode="inorder")
    assert serialized_tree == [
        4, 10, 12, 15, 18, 22, 24, 25, 31, 35, 44, 50, 66, 70, 90
    ]


def test_longer_serialize_postorder(longer_tree):
    """Tests the serialization of the longer tree with postorder traversal."""
    serialized_tree = TreeNode.traverse(longer_tree, mode="postorder")
    assert serialized_tree == [
        4, 12, 10, 18, 24, 22, 15, 31, 44, 35, 66, 90, 70, 50, 25
    ]


def test_longer_deserialize_preorder_inorder(longer_tree):
    """Writes the tree into two files and checks if they can be read back to
    create the same tree."""
    longer_tree.save_to_disk("longer_tree")

    deserialized_tree = TreeNode.parse_files(
        preorder="longer_tree.preorder",
        inorder="longer_tree.inorder")

    assert TreeNode.traverse(
        longer_tree, mode="preorder") == TreeNode.traverse(
            deserialized_tree, mode="preorder")

    assert TreeNode.traverse(
        longer_tree, mode="postorder") == TreeNode.traverse(
            deserialized_tree, mode="postorder")

    assert TreeNode.traverse(
        longer_tree, mode="inorder") == TreeNode.traverse(
            deserialized_tree, mode="inorder")

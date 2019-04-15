
# Binary Tree Implementation in Python


This module showcases how to implement a Binary Tree in Python.

It implements serialization so that a tree can be written to disk and read
back from disk.


## Setup and Running the Automated Tests

Clone the repository and set up a virtual environment in Python3.

```bash

python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
pip install -r requirements_setup.txt
pip install -r requirements_test.txt
```

Then, run the automated tests.

```bash
pytest
```

For a little verbosity:

```bash
pytest -vvv
```

### Installation

If you'd like to install this for use in other environments for whatever
reason, then:

```bash
python setup.py install # This is the usual way, but I don't recommend it.
# Instead, use the wheel.
python setup.py bdist_wheel # Make the wheel first.

pip install binary_tree --no-index --find-links=dist/
```

## What's Going On?

This module utilizes the fact that a binary tree can be serialized by
storing 2 modes of depth-first traversal. Given the preorder and inorder
traversal, or postorder and inorder traversal information, a binary
tree can be reassembled. Note that if the binary tree is also full, i.e., each
node has at least 2 children, it can be read from just the preorder and
postorder traversals. However, this isn't covered here.

This module allows users to dump the tree to disk using these two
files. This ensures that the user can read back the same tree.


## Usage

This library is written for Python 3. Do not attempt to use it with Python 2.x.

### Creating a Tree

```python

import binary_tree as bt

node = bt.TreeNode(1)
node.left_child = TreeNode(2)
node.left_child.left_child = TreeNode(4)
node.left_child.right_child = TreeNode(5)
node.right_child = TreeNode(3)
```

### Serialize the Tree

```python

bt.TreeNode.traverse(node, mode="preorder") # Get the preorder traversal
bt.TreeNode.traverse(node, mode="inorder") # Get the inorder traversal
bt.TreeNode.traverse(node, mode="postorder") # Get the postorder traversal

```

### Dump the Tree to Disk

```python

# Save preorder and inorder traversal information
node.save_to_disk(
    file_prefix="my_binary_tree",
    preorder=True,
    inorder=True,
    postorder=False)
# Save postorder and inorder traversal information
node.save_to_disk(
    file_prefix="my_binary_tree",
    preorder=False,
    inorder=True,
    postorder=True)
```

### Reading from Disk

```python

node = bt.TreeNode.parse_files(
    preorder="my_binary_tree.preorder",
    inorder="my_binary_tree.inorder")

node = bt.TreeNode.parse_files(
    postorder="my_binary_tree.postorder",
    inorder="my_binary_tree.inorder")

```

## Caveats

There *are* some caveats to this. I've listed a few that comes immediately
to mind here.


### Recursion

The major issue is recursion.

The `TreeNode` class retrieves the next items using recursion, so it hits
Python's maximum recursion limit fairly quickly. This limit is a way of preventing
stack overflow due to recursion. Python does not optimize tail recursion.
This is a huge limiting factor with respect to the size of the trees. While
it is not theoretically impossible to implement tail recursion, as I have
tried in the rudimentary `binary_tree.tail_call_optimized.tail_call_optimized`
decorator, it comes with its own baggage.

However, it *is* possible to get across this limitation, by setting
a higher recursion limit. That can be done thus:

```python
import sys
sys.setrecursionlimit(5000)
```

However, note that doing so isn't really recommended unless you know the
size of your tree and the depth of your recursion beforehand.

### Disk and Memory Utilization

Another major caveat is that the retrieval is now only as fast the disk you are
reading from. Additionally, if you're reading the entire tree to memory,
if the tree has above 1 billion nodes, you may have some issues with memory.

Since there are 2 files involved, the memory requirement is 2n where n is the
size of the tree. This is hardly an efficient problem.

I could also implement a memory map to solve that issue. Python comes with
a built-in ``mmap`` module to achieve something of this sort. ``mmap`` files
seem to support regex and other file seeking modes. I am, however,
unaware of its own caveats.

Since this problem required me to use my own ways of writing and reading a
file, I used that instead. I am fairly certain ``mmap`` could surely solve
the problems that users will indeed face with regards to the loading and
unloading of the tree.

### Speed

*Profile data for the ``test_giant_deserialize_preorder_inorder`` test*

| ncalls | tottime | percall | cumtime | percall filename:lineno(function)                                    |
|--------|---------|---------|---------|----------------------------------------------------------------------|
| 1      | 0.000   | 0.000   | 1.225   | 1.225 runner.py:118(pytest_runtest_call)                             |
| 1      | 0.000   | 0.000   | 1.225   | 1.225 python.py:1436(runtest)                                        |
| 1      | 0.000   | 0.000   | 1.225   | 1.225 hooks.py:275(__call__)                                         |
| 1      | 0.000   | 0.000   | 1.225   | 1.225 manager.py:65(_hookexec)                                       |
| 1      | 0.000   | 0.000   | 1.225   | 1.225 manager.py:59()                                                |
| 1      | 0.000   | 0.000   | 1.225   | 1.225 callers.py:157(_multicall)                                     |
| 1      | 0.000   | 0.000   | 1.225   | 1.225 python.py:156(pytest_pyfunc_call)                              |
| 1      | 0.000   | 0.000   | 1.225   | 1.225 test_serialize.py:229(test_giant_deserialize_preorder_inorder) |
| 1      | 0.000   | 0.000   | 1.215   | 1.215 tree_node.py:211(parse_files)                                  |
| 1001/1 | 0.016   | 0.000   | 1.213   | 1.213 tree_node.py:113(load)                                         |
| 500    | 0.677   | 0.001   | 0.677   | 0.001 tree_node.py:149()                                             |
| 500    | 0.517   | 0.001   | 0.517   | 0.001 tree_node.py:163()                                             |
| 4004/4 | 0.005   | 0.000   | 0.008   | 0.002 tree_node.py:42(traverse)                                      |
| 1      | 0.001   | 0.001   | 0.007   | 0.007 tree_node.py:81(save_to_disk)                                  |
| 1001   | 0.002   | 0.000   | 0.002   | 0.000 {method 'index' of 'list' objects}                             |
| 4000   | 0.002   | 0.000   | 0.002   | 0.000 {method 'extend' of 'list' objects}                            |
| 1001   | 0.001   | 0.000   | 0.001   | 0.000 tree_node.py:11(__init__)                                      |
| 1      | 0.000   | 0.000   | 0.001   | 0.001 tree_node.py:227()                                             |
| 1      | 0.000   | 0.000   | 0.001   | 0.001 tree_node.py:233()                                             |
| 2005   | 0.001   | 0.000   | 0.001   | 0.000 {method 'format' of 'str' object                               |

As you can see, the longest calls are associated with the
python recursion. Instead, I could rewrite this module using cython and
gain a good speed up. Numba is another possibility.

I worry that this module will definitely have issues when dealing with upwards
of 100 million nodes.

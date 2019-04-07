
# Binary Search Tree Implementation in Python


This module showcases how to implement a Binary Search Tree in Python.

It implements serialization so that a tree can be written to a file and read
back from said file.


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

## What's Going On?

This module serializes and writes a Binary Search Tree into a cached file. It
uses Python's `shelve` module, a module that allows us to implement database-
like persistence on disk to retrieve Python objects. The advantage of using
such an approach ensures that the entire tree is not loaded in memory all the
time. Additionally, this allows us to use large trees.


## Usage

This library is written for Python 3. Do not attempt to use it with Python 2.x.

### Creating a Tree

```python

import binary_search_tree as bst

tree = bst.BinarySearchTree(cache="my_cached_file.db")
tree[0] = "zero"
tree[1] = "one"
tree[2] = "two"
tree[42] = "forty-two"
```

### Reading from a cache

```python
import binary_search_tree as bst

tree = bst.BinarySearchTree(cache="my_cached_file.db")
print(tree[0])
# outputs "zero"
print(tree[42])
#outputs "forty-two"
```

## Caveats

There *are* some caveats to this. Python's recursion limit is the biggest one.
The `TreeNode` class retrieves the next items using recursion, so it hits
Python's maximum recursion limit fairly quickly. This limit is a way of preventing
stack overflow due to recursion, Python does not optimize tail recursion. However,
it *is* possible to get across this limitation, by setting a higher recursion
limit. That can be done thus:

```python
import sys
sys.setrecursionlimit(5000)
```

However, note that doing so isn't really recommended unless you know the size of
your tree and the depth of your recursion beforehand.

I've implemented a rudimentary `@tail_call_optimized` decorator in this
codebase but it is a small fix.

Another caveat is that the retrieval is now only as fast the disk you are
reading from. I'd instead write to a database since most databases
use a manner of b-trees for their indexed columns.


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

There *are* some caveats to this.

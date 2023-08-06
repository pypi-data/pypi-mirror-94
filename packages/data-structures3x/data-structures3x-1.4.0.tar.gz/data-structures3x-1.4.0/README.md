# Python basic data structures implementations

The **data_structures3x** is a python package with 3 of the most basic data structures. The package would keep updating as python itself updates to higher versions.

It contains the following data structures:

- Binary Tree
- Linked List
- Hashmap


# Installation
If not already, [install pip](https://pip.pypa.io/en/stable/installing/)

Install the package with `pip` or `pip3`:

```bash
pip install data-structures3x
```

# Usage
## See more examples at [My Docs](https://harvard90873.readthedocs.io/en/latest/Python%20Data%20Structures%203x.html)
### Example of a linked list:

```Python
from dt_structures3x.linkedlist import Item
# linked list
root = Item(10)
root.appendChild(Item(17), Item(19))
root.display()
```
Output:
```Python
10 -> 17 -> 19
```

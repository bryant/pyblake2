# pyblake2

Implementation of (BLAKE2)[http://blake2.net] in pure Python.

## Installation

```shell
$  cd /path/to/pyblake2
$  py.test # tests require pytest
$  python setup.py install
```

## Usage

```python
>>> from pyblake2 import blake2
>>> blake2("a random string")
'e9a5452806b05469d9882d0e625c7ea73a5b5f7d678e0ecc0c0b002a62c14c459ab17a300f73994d8090d3c8679756339ad46abe705a4e378fbeca22c2a270a1'
```

## TODO

-   speed
-   blake2s
-   salts
-   tree hashing mode

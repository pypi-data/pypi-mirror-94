# t64

This Python module enables read access to C64s tape container files (.t64).

It provides methods to list and extract the files stored within a container, only PRG files are currently supported.


## Examples

Classes reside in the `t64` module, the whole module may be imported or just those definitions referenced by the user.

### Displaying the contents of a container

To perform a directory list

```python
from t64 import T64ImageReader

with T64ImageReader('example.t64') as t:
    for line in t.directory():
        print(line)
```


## TODO

- detailed documentation
- better docstrings
- more examples

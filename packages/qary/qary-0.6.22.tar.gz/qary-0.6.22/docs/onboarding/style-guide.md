# Style Guide

## Python

### PEP8 

All python code should follow most of the [PEP8 guidlines](https://www.python.org/dev/peps/pep-0008/) except:

* line length can be as long as 130 characters

### Best practices

* McCabe complexity (number of `if` conditionals in a function) can be up to 13 (fewer is better)
* try not to use global variables unless you can't think of another way to do it
* paths should all be defined based on a `BASE_DIR` or `DATA_DIR` path defined in a `constants.py`

### Style points

In addition, you get extra "style points" ;) if you:

* Use the double-quote character (`"`) to indicate human-readable strings
* Use the single-quote character (`'`) to indicate machine-readable strings
* use `pathlib.Path()` rather than `os.path.join`: `pathlib.Path(DATA_DIR, 'subdir', 'filename.txt')`
* use `log = logging.getLogger(_name_)` and `log.debug("message")` rather than `print("message")` for debugging 
* use f-strings rather than `%` strings. F-strings look like this: 

```python
x = "world"
print(f"Hello {x}!")
```

## Docstrings

All function and class definitions and `.py` files (modules) should have a docstring.

Ideally the docstring should be similar to the [Napolean style](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html) favored by Google developers, except:

Examples should be valid doctests like:

```python
>>> add(1, 2)
3
```


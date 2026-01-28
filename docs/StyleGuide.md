# Style Guide
Written by Jake Touchet

## Python
This project is written purely in Python. Thus, this document provides a
list of guidelines to follow when writing Python code.

The project is written as a **package** and thus must be executable as a
module. 
Ex. `python -m b4igo_email_agent.subpackage.foo`

Each domain must have an `__init__.py` file to make it a subpackage.

### Type Hinting
All functions should be **fully type-hinted**. This includes both the inputs
and outputs in the function signature. 

```python
def test(a: int, b: str) -> Tuple[int, str]:
    """..."""
    return a, b
```

To make sure your code is properly typed, you should use your IDE to
ensure at least **standard** type checking. In VS Code, this is
accomplished through the "Type Checking Mode" setting.

![Type checking setting](./images/type.png)

### Function/Class/Module Documentation

Every **public function** must have a  document string in the
[Google format](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html) with at least these sections:

```python
def function_with_types_in_docstring(param1, param2):
    """Example function with types documented in the docstring.

    Longer, multiline description...
    blah blah blah...
    blah blah blah...

    Args:
        param1 (int): The first parameter.
        param2 (str): The second parameter.

    Returns:
        bool: The return value. True for success, False otherwise.

    """
```

Additional notes can be added in a `Notes` section, and any errors
raised must be listed in a `Raises` section.

**Private functions** do not always need a document string. Small
private functions with good names and function signatures are often
descriptive enough by themselves.

More complex private functions should be documented in
the Numpy format. However, the sections one includes are optional.

**Classes** must have a class string with at least a summary line.
A list of the attributes is not needed. However, one must put a
class/instance attribute's documentation in a string under its declaration. This allows
modern IDEs to display the documentation of an attribute on hover.

```python
class Car:
    """
    Object containing attributes of a car.
    """

    def __init__(...):
        self.color: str = "blue"
        """The car's color"""
        self.num_wheels: int = 85
        """Count of the car's wheels."""

```

Finally, **modules** must have a module string at the top of the file
containing at least a summary line.

```python
"""
Run main loop of codebase.

...
"""
```

## Style tools

This repository implements a variety of tools that automatically enforce
certain style constraints: 

- **isort**: Sorts and organizes imports
- **black**: Python code formatter
- **flake8**: Linting and style checking
- **mypy**: Static type checker

These are integrated as pre-commit hooks, but each has a vscode
extension that can allow one to run them dynamically while coding.

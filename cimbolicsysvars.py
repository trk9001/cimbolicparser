"""Example file to demonstrate the mapping of system-level variables.

This file demonstrate the usage of a dictionary to map actions (values or
callables) to system-defined (or more accurately, developer-defined variables).
Please note that the name of the file and the name of the dictionary MUST BE AS
IS SHOWN HERE.

While the keys of the dictionary are the variables' names, the value is a tuple
whose first item is the action (value or callable) that results in a value
being substituted for the variable, and whose second item is a list of argument
names (as strings) that a callable may take. The latter can be empty.
"""


def dummy_function(arg=None, another_arg=None):
    """Dummy callable that takes arguments."""
    return arg and another_arg


system_defined_variables = {
    'DUMMY_VAR': (dummy_function, ['arg', 'another_arg']),
}

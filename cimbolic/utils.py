import importlib.util
import os.path
from typing import Dict, Tuple, Union

import lazy_import
from django.conf import settings

from . import SYSTEM_DEFINED_VARIABLE_FILE_NAME

Variable = lazy_import.lazy_module('cimbolic.models.Variable')
Formula = lazy_import.lazy_module('cimbolic.models.Formula')


def get_system_defined_variables() -> Dict:
    """Read the file in which system-defined variables are stored and return them."""
    file_path = os.path.join(settings.BASE_DIR, SYSTEM_DEFINED_VARIABLE_FILE_NAME)
    module_name = ''.join(SYSTEM_DEFINED_VARIABLE_FILE_NAME.split('.')[:-1])
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.system_defined_variables


def clean_variable_name(var: str) -> str:
    """Clean a variable name."""
    return var.lstrip('$')


def variable_exists(var: str) -> bool:
    """Check whether a variable of the given name exists."""
    var = clean_variable_name(var)
    try:
        Variable.objects.get(name=var)
    except Variable.DoesNotExist:
        return False
    else:
        return True


def create_variable(var: str) -> 'Variable':
    """Create a user-defined variable with the given name."""
    pass


def attach_formula_to_variable(var: Union[str, 'Variable'], formula: Tuple[str, str], priority: int) -> 'Formula':
    """Create and attach a formula to the given variable."""
    pass


# TODO: Complete interfaces for variable creation.
# TODO: Create interfaces for variable maintenance and deletion.
# TODO: Add the interfaces to __init__.py

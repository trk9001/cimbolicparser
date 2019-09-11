import importlib.util
import os.path
from typing import Dict

from django.conf import settings

from . import SYSTEM_DEFINED_VARIABLE_FILE_NAME


def get_system_defined_variables() -> Dict:
    """Read the file in which system-defined variables are stored and return them."""
    file_path = os.path.join(settings.BASE_DIR, SYSTEM_DEFINED_VARIABLE_FILE_NAME)
    module_name = ''.join(SYSTEM_DEFINED_VARIABLE_FILE_NAME.split('.')[:-1])
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.system_defined_variables

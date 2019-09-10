import importlib.util
import os.path
from typing import Dict

from django.conf import settings


def get_system_defined_variables() -> Dict:
    """Read the file in which system-defined variables are stored and return """
    system_defined_variable_file_name = 'cimbolicsysvars.py'
    file_path = os.path.join(settings.BASE_DIR, system_defined_variable_file_name)
    module_name = ''.join(system_defined_variable_file_name.split('.')[:-1])
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.system_defined_variables

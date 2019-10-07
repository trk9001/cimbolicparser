import os
from importlib import util as import_util
from typing import Any, Dict, List, Tuple

from django.conf import settings

# Allow referencing by app name only in INSTALLED_APPS
default_app_config = 'cimbolic.apps.CimbolicConfig'

# Name of the file where system variables are defined
SYSTEM_VARIABLES_FILE = 'cimbolic_vars.py'


def get_system_variables() -> Dict[str, Tuple[Any, List[str]]]:
    """Read the file in which system-sourced variables are stored and return them."""
    file_path = os.path.join(settings.BASE_DIR, SYSTEM_VARIABLES_FILE)
    module_name = ''.join(SYSTEM_VARIABLES_FILE.split('.')[:-1])
    spec = import_util.spec_from_file_location(module_name, file_path)
    module = import_util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.system_variables


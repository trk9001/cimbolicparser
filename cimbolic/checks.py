import os.path

from django.conf import settings
from django.core.checks import ERROR

from .utils import SYSTEM_DEFINED_VARIABLE_FILE_NAME


def check_for_system_defined_variable_file(app_configs, **kwargs):
    """Custom system check for the file that contains sys-def variables."""
    errors = []
    file_path = os.path.join(settings.BASE_DIR, SYSTEM_DEFINED_VARIABLE_FILE_NAME)
    if not os.path.exists(file_path):
        errors.append(
            ERROR(
                'The file in which system-defined variables are stored wasn\'t found',
                hint=f'Make sure the {SYSTEM_DEFINED_VARIABLE_FILE_NAME} file exists in the project\'s root directory',
                id='cimbolic.E001',
            )
        )
    return errors

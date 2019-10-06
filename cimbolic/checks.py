import os.path

from django.conf import settings
from django.core.checks import Error

from . import SYSTEM_VARIABLES_FILE


def check_for_system_variables_file(app_configs, **kwargs):
    """Custom system check for the file that contains system-sourced variables."""
    errors = []
    file_path = os.path.join(settings.BASE_DIR, SYSTEM_VARIABLES_FILE)
    if not os.path.exists(file_path):
        errors.append(
            Error(
                "The file in which system-sourced variables are stored wasn't found",
                hint=f"Make sure the {SYSTEM_VARIABLES_FILE} file exists in the project's root directory",
                id='cimbolic.E001',
            )
        )
    return errors

from pathlib import Path

import pytest
from django.conf import settings
from django.core.checks import Error

from cimbolic import SYSTEM_VARIABLES_FILE
from cimbolic.checks import check_for_system_variables_file


@pytest.fixture
def remove_file_temporarily():
    """Temporarily remove the check's referenced file for testing."""
    # Setup
    cimbolic_vars_py = Path(settings.BASE_DIR) / SYSTEM_VARIABLES_FILE
    renamed_file = Path(settings.BASE_DIR) / f'{SYSTEM_VARIABLES_FILE}.tmp'
    cimbolic_vars_py.rename(renamed_file)

    yield None

    # Teardown
    renamed_file.rename(cimbolic_vars_py)


def test_check_for_system_variables_file_while_file_exists():
    """Test the check while the file exists."""
    errors = check_for_system_variables_file(None)
    assert errors == []


@pytest.mark.usefixtures('remove_file_temporarily')
def test_check_for_system_variables_file_while_file_exists_not():
    """Test the check while the file doesn't exist."""
    errors = check_for_system_variables_file(None)
    expected_errors = [
        Error(
            "The file in which system-sourced variables are stored wasn't found",
            hint=f"Make sure the {SYSTEM_VARIABLES_FILE} file exists in the project's root directory",
            id='cimbolic.E001',
        ),
    ]
    assert errors == expected_errors

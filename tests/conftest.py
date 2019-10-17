from pathlib import Path
from textwrap import dedent

import pytest
from django.conf import settings

from cimbolic import SYSTEM_VARIABLES_FILE


@pytest.fixture(scope='session')
def temporary_test_file_setup():
    """Set up a temporary cimbolic_vars.py file for testing."""
    # Setup
    cimbolic_vars_py = Path(settings.BASE_DIR) / SYSTEM_VARIABLES_FILE
    renamed_file = Path(settings.BASE_DIR) / f'{SYSTEM_VARIABLES_FILE}.tmp'
    cimbolic_vars_py.rename(renamed_file)
    temporary_test_file_contents = dedent(
        """\
        def func(kwarg1, kwarg2):
            return int(kwarg1) + int(kwarg2)


        system_variables = {
            'TEST_CALLABLE': (func, ['kwarg1', 'kwarg2']),
            'TEST_LITERAL': (420, []),
        }
        """
    )
    with cimbolic_vars_py.open('w', encoding='utf-8') as f:
        f.write(temporary_test_file_contents)

    yield None

    # Teardown
    renamed_file.replace(cimbolic_vars_py)

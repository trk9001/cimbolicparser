import textwrap
from pathlib import Path

import pytest
from django.conf import settings

from cimbolic import get_system_variables, SYSTEM_VARIABLES_FILE


@pytest.fixture
def temporary_test_file_setup():
    """Set up a temporary cimbolic_vars.py file for testing."""
    cimbolic_vars_py = Path(settings.BASE_DIR) / SYSTEM_VARIABLES_FILE
    renamed_file = Path(settings.BASE_DIR) / f'{SYSTEM_VARIABLES_FILE}.tmp'
    cimbolic_vars_py.rename(renamed_file)
    temporary_test_file_contents = textwrap.dedent(
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

    renamed_file.replace(cimbolic_vars_py)


@pytest.mark.usefixtures('temporary_test_file_setup')
def test_reading_system_variables_dict():
    """Test whether the system_variables dict is correctly read."""
    system_variables = get_system_variables()
    assert list(system_variables.keys()) == ['TEST_CALLABLE', 'TEST_LITERAL']
    assert callable(system_variables['TEST_CALLABLE'][0])
    assert system_variables['TEST_CALLABLE'][1] == ['kwarg1', 'kwarg2']
    assert system_variables['TEST_LITERAL'] == (420, [])

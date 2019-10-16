import os
import textwrap

import pytest
from django.conf import settings

from cimbolic import get_system_variables


@pytest.fixture
def temporary_test_file_setup():
    """Set up a temporary cimbolic_vars.py file for testing."""
    cimbolic_vars_py_path = os.path.join(settings.BASE_DIR, 'cimbolic_vars.py')
    renamed_file_path = os.path.join(settings.BASE_DIR, 'cimbolic_vars.py.tmp')
    os.rename(cimbolic_vars_py_path, renamed_file_path)
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
    with open(cimbolic_vars_py_path, 'w', encoding='utf-8') as f:
        f.write(temporary_test_file_contents)
    yield None
    os.remove(cimbolic_vars_py_path)
    os.rename(renamed_file_path, cimbolic_vars_py_path)


@pytest.mark.usefixtures('temporary_test_file_setup')
def test_reading_system_variables_dict():
    """Test whether the system_variables dict is correctly read."""
    system_variables = get_system_variables()
    assert list(system_variables.keys()) == ['TEST_CALLABLE', 'TEST_LITERAL']
    assert callable(system_variables['TEST_CALLABLE'][0])
    assert system_variables['TEST_CALLABLE'][1] == ['kwarg1', 'kwarg2']
    assert system_variables['TEST_LITERAL'] == (420, [])

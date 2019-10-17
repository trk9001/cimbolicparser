import pytest

from cimbolic import get_system_variables


@pytest.mark.usefixtures('temporary_test_file_setup')
def test_reading_system_variables_dict():
    """Test whether the system_variables dict is correctly read."""
    system_variables = get_system_variables()
    assert list(system_variables.keys()) == ['TEST_CALLABLE', 'TEST_LITERAL']
    assert callable(system_variables['TEST_CALLABLE'][0])
    assert system_variables['TEST_CALLABLE'][1] == ['kwarg1', 'kwarg2']
    assert system_variables['TEST_LITERAL'] == (420, [])

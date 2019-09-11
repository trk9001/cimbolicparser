from typing import Tuple, Union

from .exceptions import VariableNotFoundError
from .models import Variable, Formula


def clean_variable_name(var: str) -> str:
    """Clean a variable name."""
    return var.lstrip('$')


def variable_exists(var: str) -> bool:
    """Check whether a variable of the given name exists."""
    var = clean_variable_name(var)
    try:
        Variable.objects.get(name=var)
    except Variable.DoesNotExist:
        return False
    else:
        return True


def create_variable(name: str, source_model: str, description: str = '',
                    type: str = Variable.USER_DEFINED, is_active: bool = True) -> Variable:
    """Create a user-defined variable with the given name."""
    var = Variable.objects.create(
        name=name,
        source_model=source_model,
        description=description,
        type=type,
        is_active=is_active
    )
    return var


def attach_formula_to_variable(var: Union[str, Variable], formula: Tuple[str, str],
                               priority: int, is_active: bool = True) -> Formula:
    """Create and attach a formula to the given variable."""
    if isinstance(var, str):
        try:
            variable = Variable.objects.get(name=clean_variable_name(var))
        except Variable.DoesNotExist:
            raise VariableNotFoundError(f'Variable {var} does not exist in the database')
    else:
        variable = var

    condition, rule = formula
    formula = Formula.objects.create(
        variable=variable,
        condition=condition,
        rule=rule,
        priority=priority,
        is_active=is_active
    )
    return formula


# TODO: Create interfaces for variable maintenance and deletion.
# TODO: Add the interfaces to __init__.py

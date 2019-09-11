from typing import Tuple, Union

from .exceptions import VariableNotFoundError
from .models import Variable, Formula


def _clean_variable_name(var: str) -> str:
    """Clean a variable name."""
    return var.lstrip('$')


def _clean_to_variable(var: Union[str, Variable]) -> Variable:
    """Get a Variable referenced by a string (or not) and return it."""
    if isinstance(var, str):
        var = _clean_variable_name(var)
        try:
            variable = Variable.objects.get(name=var)
        except Variable.DoesNotExist:
            raise VariableNotFoundError(f'Variable ${var} does not exist in the database')
    else:
        variable = var
    return variable


def variable_exists(var: str) -> bool:
    """Check whether a variable of the given name exists."""
    var = _clean_variable_name(var)
    try:
        Variable.objects.get(name=var)
    except Variable.DoesNotExist:
        return False
    else:
        return True


def create_variable(name: str, source_model: str, description: str = None,
                    type: str = Variable.USER_DEFINED, is_active: bool = True) -> Variable:
    """Create a user-defined variable with the given name."""
    var = Variable.objects.create(
        name=name,
        source_model=source_model,
        description=description or '',
        type=type,
        is_active=is_active
    )
    return var


def attach_formula_to_variable(variable: Union[str, Variable], formula: Tuple[str, str], priority: int) -> Formula:
    """Create and attach a formula to the given variable."""
    variable = _clean_to_variable(variable)
    condition, rule = formula
    formula = Formula.objects.create(
        variable=variable,
        condition=condition,
        rule=rule,
        priority=priority,
    )
    return formula


def update_variable(variable: Union[str, Variable], name: str = None, source_model: str = None,
                    description: str = None, type: str = None, is_active: bool = None) -> Variable:
    """Update a user-defined variable with the given name."""
    fields = {}
    if name:
        fields['name'] = name
    if description:
        fields['description'] = description
    if type:
        fields['type'] = type
    if source_model:
        fields['source_model'] = source_model
    if is_active:
        fields['is_active'] = is_active
    variable = _clean_to_variable(variable)
    for key in fields:
        setattr(variable, key, fields[key])
    variable.save(update_fields=list(fields.keys()))
    return variable


def delete_variable(variable: Union[str, Variable], mark_inactive_only: bool = False) -> str:
    """Delete/deactivate a variable and return its name."""
    variable = _clean_to_variable(variable)
    if mark_inactive_only:
        variable.is_active = False
        variable.save(update_fields=['is_active'])
    else:
        variable.delete()
    return variable.name


# TODO: Create interfaces for variable maintenance and deletion.
# TODO: Add the interfaces to __init__.py

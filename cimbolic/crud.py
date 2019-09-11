from decimal import Decimal
from typing import Any, Dict, List, Tuple, Union

from django.core.exceptions import FieldDoesNotExist

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


def _clean_to_formula(variable: Union[str, Variable] = None, formula: Formula = None,
                      condition: str = None, priority: int = None) -> Formula:
    """Get the referenced Formula and return it."""
    arguments_valid = True
    if formula is None:
        if variable is not None:
            variable = _clean_to_variable(variable)
            if condition is not None:
                formula = variable.formulae.get(condition=condition)
            elif priority is not None:
                formula = variable.formulae.get(priority=priority)
            else:
                arguments_valid = False
        else:
            arguments_valid = False
    if not arguments_valid:
        raise TypeError('Arguments required to identify a Formula: Formula or (variable and (condition or priority))')
    else:
        return formula


def check_variable_exists(var: str) -> bool:
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
        name=_clean_variable_name(name),
        source_model=source_model,
        description=description or '',
        type=type,
        is_active=is_active
    )
    return var


def create_formula_of_variable(variable: Union[str, Variable], formula: Union[Formula, Tuple[str, str]],
                               priority: int) -> Formula:
    """Create and attach a formula to the given variable."""
    variable = _clean_to_variable(variable)
    if isinstance(formula, tuple):
        condition, rule = formula
        formula = Formula.objects.create(
            variable=variable,
            condition=condition,
            rule=rule,
            priority=priority,
        )
    else:
        variable.formulae.add(formula)
    return formula


def read_variable(variable: Union[str, Variable], context: Dict[str, Any] = None) -> Union[int, Decimal]:
    """Fetch a variable's value from the database and return it."""
    variable = _clean_to_variable(variable)
    value = variable.to_value(context)
    return value


def update_variable(variable: Union[str, Variable], data: Dict[str, Any]) -> Tuple[Variable, List[str]]:
    """Update a user-defined variable with the given name, using the data dictionary."""
    updated_fields = []
    variable = _clean_to_variable(variable)
    for key in data:
        try:
            variable._meta.get_field(key)
        except FieldDoesNotExist:
            pass
        else:
            setattr(variable, key, data[key])
            updated_fields.append(key)
    variable.save(update_fields=updated_fields)
    return variable, updated_fields


def update_formula_of_variable(data: Dict[str, Any], variable: Union[str, Variable] = None, formula: Formula = None,
                               condition: str = None, priority: int = None) -> Tuple[Formula, List[str]]:
    """Update a formula attached to the given variable, using the data dictionary."""
    formula = _clean_to_formula(variable, formula, condition, priority)

    updated_fields = []
    for key in data:
        try:
            formula._meta.get_field(key)
        except FieldDoesNotExist:
            pass
        else:
            setattr(formula, key, data[key])
            updated_fields.append(key)
    formula.save(update_fields=updated_fields)
    return formula, updated_fields


def delete_variable(variable: Union[str, Variable], mark_inactive_only: bool = False) -> str:
    """Delete/deactivate a variable and return its name."""
    variable = _clean_to_variable(variable)
    if mark_inactive_only:
        variable.is_active = False
        variable.save(update_fields=['is_active'])
    else:
        variable.delete()
    return variable.name


def delete_formula_of_variable(variable: Union[str, Variable] = None, formula: Formula = None,
                               condition: str = None, priority: int = None) -> Tuple[str, str, int]:
    """Delete the specified formula and return it's attributes."""
    formula = _clean_to_formula(variable, formula, condition, priority)
    formula.delete()
    return formula.condition, formula.rule, formula.priority


# TODO: Add the interfaces to __init__.py

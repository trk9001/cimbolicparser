import re
from decimal import Decimal
from functools import lru_cache
from typing import Any, Dict, Iterable, List, Optional, Union

from django.core.validators import MinValueValidator, RegexValidator
from django.db import models

from . import get_system_variables
from .exceptions import *
from .parsing import Condition, Rule


class Variable(models.Model):
    """Model representing metadata of a named variable."""
    SYSTEM = 'S'
    USER = 'U'

    SOURCE_CHOICES = [
        (SYSTEM, 'System'),
        (USER, 'User'),
    ]

    NONE_TYPE = ''
    MODEL_TYPE = 'M'
    MODEL_FIELD_TYPE = 'F'
    MODEL_INSTANCE_TYPE = 'I'

    RELATED_DATA_TYPE_CHOICES = [
        (NONE_TYPE, 'None'),
        (MODEL_TYPE, 'Model'),
        (MODEL_FIELD_TYPE, 'Model field'),
        (MODEL_INSTANCE_TYPE, 'Model instance'),
    ]

    name = models.CharField(
        help_text='Name of the variable (eg: BASIC, WH_1)',
        validators=[
            RegexValidator(
                r'^[a-zA-Z_][a-zA-Z0-9_]*$',
                "Must conform to the regex '^[a-zA-Z_][a-zA-Z0-9_]*$'",
            )
        ],
        max_length=100,
        unique=True,
    )
    description = models.TextField(
        help_text='A brief description of the variable',
        max_length=500,
        blank=True,
    )
    source = models.CharField(
        help_text='Whose action the variable originates from (eg: system, user)',
        choices=SOURCE_CHOICES,
        max_length=1,
    )
    related_data_type = models.CharField(
        help_text='The type of the data this variable is related to (eg: model, instance)',
        choices=RELATED_DATA_TYPE_CHOICES,
        max_length=1,
        blank=True,
    )
    related_data_path = models.CharField(
        help_text=(
            'The dotted path to the data to which this variable is related, '
            'in the format {app_label}.{model_name}[.{field_name|pk}]'
        ),
        max_length=500,
        validators=[
            RegexValidator(
                r'^\w+\.\w+(\.\w+)?$',
                "Must conform to the regex '^\\w+\\.\\w+(\\.\\w+)?$'",
            ),
        ],
        blank=True,
    )
    is_active = models.BooleanField(
        help_text='Whether the variable is currently active',
        default=True,
    )

    def __str__(self):
        return f'${self.name}'

    @property
    def related_data(self) -> Any:
        """Send a Python-object version of the variable's related data."""
        if self.related_data_type == self.NONE_TYPE:
            return None

        from django.apps import apps
        app_label, model_name, *extra = self.related_data_path.split('.')
        try:
            model = apps.get_model(app_label, model_name)
        except Exception as exc:
            raise VariableRelatedDataError(
                f"Can't retrieve model from {self} variable's "
                f"related_data_path: {self.related_data_path}"
            ) from exc

        if self.related_data_type == self.MODEL_TYPE:
            return model

        try:
            extra = extra[0]
        except IndexError as exc:
            raise VariableRelatedDataError(
                f"Missing third element from {self} variable's "
                f"related_data_path: {self.related_data_path}"
            ) from exc

        if self.related_data_type == self.MODEL_FIELD_TYPE:
            # No way to actually reference the Django model field, so pass its
            # name along with the model class so that the user can use the
            # getattr/setattr functions to get/set the field.
            if hasattr(model, extra):
                return model, extra
            raise VariableRelatedDataError(
                f"Model derived from {self} variable's "
                f"related_data_path {self.related_data_path} "
                f"doesn't have a field called {extra}"
            )

        if self.related_data_type == self.MODEL_INSTANCE_TYPE:
            try:
                instance = model.objects.get(pk=extra)
            except model.DoesNotExist as exc:
                raise VariableRelatedDataError(
                    f"Model derived from {self} variable's "
                    f"related_data_path {self.related_data_path} "
                    f"doesn't have an instance with primary key {extra}"
                ) from exc
            return instance

    def context_keys(self) -> List[str]:
        context_keys = get_all_context_keys(self)
        return context_keys

    def prioritized_formulae(self) -> Union[Iterable, models.query.QuerySet]:
        """Return a queryset of the relevant formulae sorted by priority."""
        formulae = self.formulae.order_by('priority')
        return formulae

    def to_value(self, context: Optional[Dict[str, Any]] = None) -> Union[int, Decimal]:
        """Parse the variable's formulae and return a value."""
        if self.source == self.SYSTEM:
            sys_vars = get_system_variables()
            try:
                result, result_args = sys_vars[self.name]
            except KeyError:
                raise VariableNotDefinedError(f'System variable {self} undefined')
            if callable(result):
                result_kwargs = {}
                context = context or {}
                for key in result_args:
                    if key in context.keys():
                        result_kwargs[key] = context[key]
                    else:
                        raise KeyError(f'Missing argument {key} to callable {result.__name__}')
                return result(**result_kwargs)
            else:
                return result

        if self.source == self.USER:
            prioritized_formulae = self.prioritized_formulae()
            if not prioritized_formulae.exists():
                raise VariableNotDefinedError(f'No formula defined for variable {self.name}')
            for formula in prioritized_formulae:
                if formula.condition_to_boolean(context):
                    result = formula.rule_to_value(context)
                    return result


class Formula(models.Model):
    """Model representing a condition-rule pair associated with a named variable."""
    variable = models.ForeignKey(
        Variable,
        help_text='Variable to which this formula is bound',
        on_delete=models.CASCADE,
        related_name='formulae',
        related_query_name='formula',
    )
    condition = models.TextField(
        help_text='Cimbolic condition for the rule to be set',
        default='NULL',
    )
    rule = models.TextField(
        help_text='Cimbolic arithmetic rule to be set',
    )
    priority = models.PositiveIntegerField(
        help_text=(
            'Set the priority of condition-checking (1 is highest) '
            '(Note: the priority of a \'NULL\' condition will automatically be set to be the lowest)'
        ),
        validators=[
            MinValueValidator(1),
        ],
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['variable', 'priority'],
                name='unique_formula_priority_per_variable',
            ),
        ]
        verbose_name_plural = 'formulae'

    def save(self, *args, **kwargs):
        # Disallow saving if no 'NULL' condition exists.
        siblings = Formula.objects.filter(variable=self.variable)
        if self.pk is not None:
            siblings = siblings.exclude(pk=self.pk)
        if self.condition != 'NULL' and not siblings.filter(condition='NULL').exists():
            raise DefaultFormulaMissingError(
                f'Default formula (with a \'NULL\' condition) is missing for variable {self.variable}'
            )
        super().save(*args, **kwargs)

        # Update the priority of the formula with the 'NULL' condition to be
        # the highest of the same variable's formulae's priorities.
        family = Formula.objects.filter(variable=self.variable)
        null_formula = family.get(condition='NULL')
        non_null_formulae = family.exclude(pk=null_formula.pk)
        max_priority = non_null_formulae.aggregate(max_p=models.Max('priority')).get('max_p')
        max_priority = max_priority or 0
        if null_formula.priority <= max_priority:
            null_formula.priority = max_priority + 1
            null_formula.save(update_fields=['priority'])

    def __str__(self):
        return f'{self.variable} > priority {self.priority}'

    def condition_to_boolean(self, context: Optional[Dict] = None) -> bool:
        """Parse the condition and return a boolean result."""
        cond = Condition(self.condition, context)
        result = cond.evaluate()
        return result

    def rule_to_value(self, context: Optional[Dict] = None) -> Union[int, Decimal]:
        """Parse the rule and evaluate it to give a result."""
        rule = Rule(self.rule, context)
        result = rule.evaluate()
        return result


named_variable_regex = re.compile(r'\$([a-zA-Z_][a-zA-Z0-9_]*)')


@lru_cache(maxsize=64)
def get_all_context_keys(variable: Variable) -> List[str]:
    """Get every context key dependency for a particular variable."""
    context_keys: List[str] = []
    if variable.source == variable.SYSTEM:
        try:
            fn, keys = get_system_variables()[variable.name]
        except KeyError:
            raise VariableNotDefinedError(f'System variable {variable} undefined')
        if callable(fn):
            context_keys.extend(keys)
    else:
        rules: List[str] = [formula.rule for formula in variable.formulae.all()]
        for rule in rules:
            named_variables = named_variable_regex.findall(rule)
            for named_var in named_variables:
                try:
                    var = Variable.objects.get(name=named_var)
                except Variable.DoesNotExist:
                    raise VariableNotFoundError(
                        f'Nonexistent variable ${named_var} referenced in rule: {rule}'
                    )
                context_keys.extend(get_all_context_keys(var))
    # Eliminate duplicates.
    context_keys = list(set(context_keys))
    return context_keys

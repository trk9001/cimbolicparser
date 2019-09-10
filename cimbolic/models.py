from decimal import Decimal
from typing import Iterable, Union

from django.core.validators import MinValueValidator, RegexValidator
from django.db import models


class Variable(models.Model):
    """Model representing metadata of a named variable."""
    TYPE_CHOICES = [
        ('sys', 'system-defined'),
        ('usr', 'user-defined'),
    ]

    name = models.CharField(
        help_text='Name of the variable (eg: BASIC)',
        max_length=80,
        unique=True,
    )
    description = models.TextField(
        help_text='A brief description of the variable',
        max_length=500,
        blank=True,
    )
    type = models.CharField(
        help_text='Whether the variable is system defined or user-created',
        choices=TYPE_CHOICES,
        max_length=3,
    )
    source_model = models.CharField(
        help_text='The model to which this variable belongs (eg: payroll.Component)',
        max_length=500,
        validators=[
            RegexValidator(r'^\w+\.\w+$'),
        ],
        blank=True,
    )
    is_active = models.BooleanField(
        help_text='Whether the variable is currently active',
        default=True,
    )

    def __str__(self):
        return f'{self.name}'

    def prioritized_formulae(self) -> Iterable:
        """Return a queryset of the relevant formulae sorted by priority."""
        formulae = self.formulae.order_by('priority')
        return formulae

    def to_value(self) -> Union[str, int, Decimal]:
        """Parse the variable's formulae and return a value."""
        for formula in self.prioritized_formulae():
            if formula.condition_to_boolean():
                result = formula.rule_to_value()
                return result
        # TODO: blah


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
            'Set the ordering of condition-checking (1 is highest) '
            '(Note: the priority of a \'NULL\' condition will automatically be set to be the lowest)'
        ),
        validators=[
            MinValueValidator(1),
        ],
    )
    is_active = models.BooleanField(
        help_text='Whether the formula is currently active',
        default=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['variable', 'priority'],
                name='unique_formula_priority_per_variable',
            ),
            models.UniqueConstraint(
                fields=['variable', 'condition'],
                name='unique_formula_condition_per_variable',
            ),
        ]
        verbose_name_plural = 'formulae'

    def save(self, *args, **kwargs):
        # Disallow saving if no 'NULL' condition exists
        siblings = Formula.objects.filter(variable=self.variable)
        if self.pk is not None:
            siblings = siblings.exclude(pk=self.pk)
        if self.condition != 'NULL' and not siblings.filter(condition='NULL').exists():
            raise Exception  # TODO: blah
        super().save(*args, **kwargs)

        # Update the priority of the formula with the 'NULL' condition to be
        # the highest of the same variable's formulae's priorities.
        family = Formula.objects.filter(variable=self.variable)
        null_formula = family.get(condition='NULL')
        non_null_formulae = family.exclude(pk=null_formula.pk)
        max_priority = non_null_formulae.aggregate(max_p=models.Max('priority')).get('max_p')
        if null_formula.priority <= max_priority:
            null_formula.priority = max_priority + 1
            null_formula.save(update_fields=['priority'])

    def __str__(self):
        return f'{self.variable} > priority {self.priority}'

    def condition_to_boolean(self) -> bool:
        """Parse the condition and return a boolean result."""
        pass

    def rule_to_value(self) -> Union[str, int, Decimal]:
        """Parse the rule and evaluate it to give a result."""
        pass

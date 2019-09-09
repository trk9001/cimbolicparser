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
        help_text='Set the ordering of condition-checking (1 is highest)',
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
        ]
        verbose_name_plural = 'formulae'

    def __str__(self):
        return f'{self.variable} > priority {self.priority}'

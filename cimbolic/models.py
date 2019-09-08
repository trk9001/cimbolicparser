from django.core.validators import RegexValidator
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
    created_at = models.DateTimeField(
        help_text='Date-time of creation',
        auto_now_add=True,
        editable=False,
    )
    last_modified_at = models.DateTimeField(
        help_text='Date-time of last modification',
        auto_now=True,
        editable=False,
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

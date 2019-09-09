# Generated by Django 2.2.5 on 2019-09-09 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cimbolic', '0002_auto_20190909_1718'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='formula',
            constraint=models.UniqueConstraint(fields=('variable', 'condition'), name='unique_formula_condition_per_variable'),
        ),
    ]

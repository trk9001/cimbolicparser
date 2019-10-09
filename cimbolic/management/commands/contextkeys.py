from argparse import ArgumentParser

from django.core.management.base import BaseCommand, CommandError

from cimbolic.models import get_all_context_keys, Variable


class Command(BaseCommand):
    """Management command to list all the context keys for a Variable."""
    help = 'Displays a set of context keys for each specified variable'

    def add_arguments(self, parser: ArgumentParser):
        parser.add_argument(
            'vars',
            nargs='+',
            help='The name of the variable',
            metavar='variable',
        )
        parser.add_argument(
            '-u', '--union',
            help='display the collective list of context keys',
            action='store_true',
        )

    def handle(self, *args, **options):
        variables = []
        for var in options['vars']:
            var_name = var.lstrip('$')
            try:
                variables.append(Variable.objects.get(name=var_name))
            except Variable.DoesNotExist:
                raise CommandError(f'Variable ${var_name} not found in the database')

        get_all_context_keys.cache_clear()
        context_key_dict = dict([
            (variable.name, set(get_all_context_keys(variable)))
            for variable in variables
        ])

        if options['union']:
            context_keys = set()
            for ck_set in context_key_dict.values():
                context_keys |= ck_set
            self.stdout.write(self.style.SUCCESS(f'- {list(context_keys)}'))

        else:
            for var in context_key_dict:
                self.stdout.write(self.style.SUCCESS(f'- ${var}'), ending=': ')
                self.stdout.write(self.style.SUCCESS(f'{list(context_key_dict[var])}'))

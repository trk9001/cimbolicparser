from django.core.management.base import BaseCommand

from cimbolic import get_system_variables
from cimbolic.models import Variable


class Command(BaseCommand):
    """Management command to populate Variable objects with system variables.

    It collects variables that are referenced in the cimbolic_vars.py file
    in the project's root directory, but whose names do not exist among the
    Variable objects. It then creates Variable objects from those variables,
    given that no clashing occurs with the existing Variable objects. If an
    inactive system-sourced Variable object exists (is_active == False), it
    also marks the Variable object as active.

    It also marks Variable objects not referenced in cimbolic_vars.py anymore
    as inactive (is_active = False). This means that the mentioned file is the
    only way for a developer to add system-sourced variables.
    """
    help = 'Loads system-sourced variables from cimbolic_vars.py into the Variable model'

    def handle(self, *args, **options):
        sys_vars = get_system_variables()

        vars_added = []
        for var in sys_vars:
            if not Variable.objects.filter(name=var).exists():
                Variable.objects.create(name=var, type=Variable.SYSTEM_DEFINED, is_active=True)
                vars_added.append(var)
            else:
                v = Variable.objects.get(name=var)
                if not v.is_active:
                    vars_added.append(v)
                    v.is_active = True
                    v.save(update_fields=['is_active'])

        if vars_added:
            self.stdout.write(self.style.SUCCESS('The following variables have been loaded or activated: '), ending='')
            for var in vars_added[:-1]:
                self.stdout.write(self.style.SUCCESS(f'{var}'), ending=', ')
            self.stdout.write(self.style.SUCCESS(f'{vars_added[-1]}'))

        vars_marked_inactive = []
        sys_vars_in_db = Variable.objects.filter(type=Variable.SYSTEM_DEFINED, is_active=True)
        for var in sys_vars_in_db:
            if var.name not in sys_vars:
                vars_marked_inactive.append(var.name)
                var.is_active = False
                var.save(update_fields=['is_active'])

        if vars_marked_inactive:
            self.stdout.write(self.style.SUCCESS('The following variables have been marked as inactive: '), ending='')
            for var in vars_marked_inactive[:-1]:
                self.stdout.write(self.style.SUCCESS(f'{var}'), ending=', ')
            self.stdout.write(self.style.SUCCESS(f'{vars_marked_inactive[-1]}'))

        if not vars_added and not vars_marked_inactive:
            return self.style.SUCCESS('Done')

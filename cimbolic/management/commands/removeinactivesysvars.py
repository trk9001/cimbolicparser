from django.core.management.base import BaseCommand

from cimbolic.models import Variable


class Command(BaseCommand):
    """Management command to delete inactive system-defined Variable objects."""
    help = 'Removes inactive (is_active == False) system-defined Variable objects.'

    def handle(self, *args, **options):
        count, _ = Variable.objects.filter(type=Variable.SYSTEM_DEFINED, is_active=False).delete()
        self.stdout.write(self.style.SUCCESS(f'Deleted {count} objects'))

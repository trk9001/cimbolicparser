from django.core.management.base import BaseCommand

from cimbolic.models import Variable


class Command(BaseCommand):
    """Management command to delete inactive system-sourced Variable objects."""
    help = 'Deletes inactive (is_active == False) system-sourced Variable objects.'

    def handle(self, *args, **options):
        count, _ = Variable.objects.filter(type=Variable.SYSTEM_DEFINED, is_active=False).delete()
        self.stdout.write(self.style.SUCCESS(f'Deleted {count} objects'))

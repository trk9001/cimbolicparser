from django.apps import AppConfig
from django.core.checks import register

from .checks import check_for_system_defined_variable_file


class CimbolicConfig(AppConfig):
    name = 'cimbolic'

    def ready(self):
        register(check_for_system_defined_variable_file)

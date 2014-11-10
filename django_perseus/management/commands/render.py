from django.core.management.base import BaseCommand

from django_perseus.utils import run_renderers, run_importers


class Command(BaseCommand):

    def handle(self, *args, **options):
        run_renderers()
        run_importers()

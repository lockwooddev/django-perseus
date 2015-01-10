from django.core.management.base import BaseCommand

from django_perseus.utils import run_renderers, run_importers, zip_dir

from optparse import make_option


class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        make_option(
            '--archive',
            action='store_true',
            dest='archive',
            default=False,
            help='Zips the result of the statically generated website'),
        make_option(
            '--filename',
            action='store',
            dest='filename',
            default=''),
    )

    def handle(self, *args, **options):
        run_renderers()
        run_importers()

        archive = options.get('archive')
        if archive:
            zip_dir(options.get('filename', 'render.zip'))

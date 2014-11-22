from django_perseus.importers.base import BaseImporter


class TestImporter(BaseImporter):

    target_dir = 'PERSEUS_SOURCE_DIR'
    source_dir = 'MEDIA_ROOT'
    sub_dirs = []

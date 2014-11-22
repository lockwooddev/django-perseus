from django.conf import settings

from django_perseus.utils import find_renderers, zip_dir
from testapp2.renderers import TestRenderer

import mock
import os
import pytest
import shutil
import zipfile


class TestUtils:

    def test_find_renderers(self, settings):
        modules = find_renderers()
        assert len(modules) == 1
        assert modules[0] == (TestRenderer)
        assert modules[0].__module__ == 'django_perseus.tests.testapp2.renderers'


class TestZipDir:

    def setup(self):
        self.filename = 'test.zip'

    def test_zip_dir_success(self):
        source_dir = settings.PERSEUS_SOURCE_DIR
        if not os.path.isdir(source_dir):
            os.makedirs(source_dir)

        subdir = os.path.join(source_dir, 'subdir')
        os.makedirs(subdir)
        open(os.path.abspath(os.path.join(source_dir, 'test1.txt')), 'a').close()
        open(os.path.abspath(os.path.join(subdir, 'test2.txt')), 'a').close()

        zip_dir(self.filename)
        new_file = os.path.join(settings.PERSEUS_BUILD_DIR, self.filename)
        assert os.path.isfile(new_file)

        with zipfile.ZipFile(new_file, 'r') as new_zip:
            namelist = new_zip.namelist()
            assert 'source/test1.txt' in namelist
            assert 'source/subdir/test2.txt' in namelist

    def test_zip_dir_source_dir_setting_none(self):
        with pytest.raises(Exception):
            with mock.patch('django_perseus.utils.settings') as settings_mock:
                settings_mock.return_value = None
                zip_dir(self.filename)

    def test_zip_dir_source_dir_not_a_directory(self):
        pass

    def test_zip_dir_build_dir_none(self):
        pass

    def teardown(self):
        if os.path.isdir(settings.PERSEUS_BUILD_DIR):
            shutil.rmtree(settings.PERSEUS_BUILD_DIR)

        if os.path.isdir(settings.PERSEUS_SOURCE_DIR):
            shutil.rmtree(settings.PERSEUS_SOURCE_DIR)

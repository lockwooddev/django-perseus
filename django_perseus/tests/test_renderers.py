from django.core.urlresolvers import reverse
from django.conf import settings as conf

from django_perseus.exceptions import RendererException
from django_perseus.renderers.default import DefaultRenderer
from .utils import is_file, is_dir

import os
import pytest
import shutil


class TestDefaultRenderer:

    def remove_dirs(self):
        # make sure source dir is empty
        source_dir = conf.PERSEUS_SOURCE_DIR
        if os.path.isdir(source_dir):
            shutil.rmtree(source_dir)

    def setup(self):
        self.remove_dirs()

        class TestRenderer(DefaultRenderer):

            def paths(self):
                return [
                    reverse('index'),
                    reverse('test'),
                    reverse('testapp2:index'),
                    reverse('testapp2:sub1'),
                    reverse('testapp2:sub2', kwargs={'pk': 1}),
                    reverse('testapp2:sub2', kwargs={'pk': 2}),
                    reverse('testapp2:sub3', kwargs={'pk': 1}),
                    reverse('testapp2:sub4', kwargs={'pk': 1}),
                    reverse('testapp2:sub5', kwargs={'pk': 1, 'id': 1}),
                ]

        self.renderer = TestRenderer()

    def test_generate(self, settings):
        settings.RENDER_STATIC = True
        self.renderer.generate()

        perseus_dir = settings.PERSEUS_SOURCE_DIR

        assert is_file(perseus_dir, 'index.html')
        assert is_file(perseus_dir, 'test.html')
        assert is_file(perseus_dir, 'testapp2.html')
        assert is_file(perseus_dir, 'testapp2', 'test.html')
        assert is_file(perseus_dir, 'testapp2', 'test', '1.html')
        assert is_file(perseus_dir, 'testapp2', 'test', '2.html')
        assert is_file(perseus_dir, 'testapp2', 'test', '1', 'test.html')
        assert is_file(perseus_dir, 'testapp2', 'test', '1', 'test', '1.html')

        assert is_dir(perseus_dir)
        assert is_dir(perseus_dir, 'testapp2')
        assert is_dir(perseus_dir, 'testapp2', 'test')
        assert is_dir(perseus_dir, 'testapp2', 'test', '1')

    def test_generate_path_not_200(self, settings):
        settings.RENDER_STATIC = True

        class FailRenderer(DefaultRenderer):

            def paths(self):
                return [
                    reverse('not_found'),
                ]

        self.renderer = FailRenderer()

        with pytest.raises(RendererException):
            self.renderer.generate()

    def teardown(self):
        self.remove_dirs()

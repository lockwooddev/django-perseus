from django_perseus.utils import find_renderers

from testapp2.renderers import TestRenderer


class TestUtils:

    def test_find_renderers(self, settings):
        modules = find_renderers()
        assert len(modules) == 1
        assert modules[0] == (TestRenderer)
        assert modules[0].__module__ == 'django_perseus.tests.testapp2.renderers'

from django_perseus.renderers.default import DefaultRenderer


class TestRenderer(DefaultRenderer):

    def paths(self):
        return ['/']

renderers = [TestRenderer, ]

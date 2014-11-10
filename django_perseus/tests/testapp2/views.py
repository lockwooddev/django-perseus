from django.views.generic.base import TemplateView


class DummyView(TemplateView):

    template_name = 'dummy.html'

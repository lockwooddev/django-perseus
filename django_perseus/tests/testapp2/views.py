from django.views.generic.base import TemplateView
from django.http import HttpResponse


class DummyView(TemplateView):

    template_name = 'dummy.html'


class NotFoundView(TemplateView):

    template_name = 'dummy.html'

    def get(self, request, *args, **kwargs):
        return HttpResponse('', status=404)

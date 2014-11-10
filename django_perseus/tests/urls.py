# from django.conf import settings
from django.conf.urls import include, patterns, url

from testapp2.views import DummyView


urlpatterns = patterns(
    '',
    url(r'^$', DummyView.as_view(), name='index'),
    url(r'^test/$', DummyView.as_view(), name='test'),
    url(r'^testapp2/', include('django_perseus.tests.testapp2.urls', namespace='testapp2')),
)


# if settings.DEBUG:
#     urlpatterns += patterns(
#         '',
#         (r'^%s(?P<path>.*)$' % settings.MEDIA_URL.strip('/'),
#             'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
#     )

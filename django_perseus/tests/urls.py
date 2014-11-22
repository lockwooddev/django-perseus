from django.conf.urls import include, patterns, url

from testapp2.views import DummyView, NotFoundView


urlpatterns = patterns(
    '',
    url(r'^$', DummyView.as_view(), name='index'),
    url(r'^test/$', DummyView.as_view(), name='test'),
    url(r'^testapp2/', include('django_perseus.tests.testapp2.urls', namespace='testapp2')),
    url(r'^not_found/$', NotFoundView.as_view(), name='not_found'),
)

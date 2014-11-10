from django.conf.urls import patterns, url

from .views import DummyView


urlpatterns = patterns(
    '',
    url(r'^$', DummyView.as_view(), name='index'),
    url(r'^test/$', DummyView.as_view(), name='sub1'),
    url(r'^test/(?P<pk>[\d]+)/$', DummyView.as_view(), name='sub2'),
    url(r'^test/(?P<pk>[\d]+)$', DummyView.as_view(), name='sub3'),
    url(r'^test/(?P<pk>[\d]+)/test/$', DummyView.as_view(), name='sub4'),
    url(r'^test/(?P<pk>[\d]+)/test/(?P<id>[\d]+)/$', DummyView.as_view(), name='sub5'),
)


from django.conf.urls import patterns, url
from wstaw import views


urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<page>\d+)/', views.page, name='page')
)

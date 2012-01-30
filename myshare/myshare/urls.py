from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'index', name='index'),
    url(r'^page$', 'page', name='page')
)

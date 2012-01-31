from django.conf.urls.defaults import *
from django.contrib import admin

from app.views import MyShareHistory, MyShares
from myshare.views import new
admin.autodiscover()

urlpatterns = patterns('',
                       
     url(r'^$', 'app.views.home', name='example-home'),
     url(r'^/api/$', 'app.views.example_api', name='example-api'),
     url(r'^/history/$', MyShareHistory.as_view() , name='example-history'),
     url(r'^/new/$', 'myshare.views.new', name='myshare-new'),
     url(r'^myshare/$', MyShares.as_view(), name='myshare-shares'), 
     url(r'^admin/$', include(admin.site.urls)),
    )


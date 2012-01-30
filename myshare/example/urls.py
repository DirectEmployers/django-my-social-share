from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin

from app.views import home, MyShareHistory, MyShares
from myshare.views import new
admin.autodiscover()

urlpatterns = patterns('',
                       
     url(r'^$', 'app.home', name='home'),
     url(r'^/api/(?P<url>.*)$', 'app.api', name='api'),
     url(r'^/history/', MyShareHistory.as_view() , name='history'),
     url(r'^/new/', new, name='new'),
     url(r'^myshare/', MyShares.as_view(), name='share'), 
     #url(r'', 'myshare.urls'),
     url(r'^admin/', include(admin.site.urls)),
    )


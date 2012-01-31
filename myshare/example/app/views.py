"""
views.py - implements views for django-my-social-share example app
"""
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.views.generic import ListView, FormView
from django.template import RequestContext
from django.utils.translation import ugettext, ugettext_lazy as _
from requests import get
from BeautifulSoup import BeautifulSoup
from forms import MakeShare
from django.core.validators import URLValidator
from myshare.models import History, Share


class MyShareHistory(ListView):
    """implements a simple history view"""
    context_object_name = History
    model = History
    
class MyShares(ListView):
    """implements a list of all shares"""
    context_object_name = Share
    model = Share

def home(request):
    """Implements home page view"""
    return render(request, 'home.html', {'title':_("Example App Home")})
    
def example_api(request):
    """Implements a simple api for the bookmarket"""
    if request.method == "GET":
        HttpResponseForbidden(_("GET Method not allowed.")
        try: 
            URLValidator(url)
        except:
            HttpResponseBadRequest(_("Bad URL"))
        else:
            return render(request, "/new", {"url":url})
    else:
        HttpResponseForbidden(_("No URL Provided"))

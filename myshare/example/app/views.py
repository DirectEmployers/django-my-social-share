"""
views.py - implements views for django-my-social-share example app
"""

from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.views.generic import ListView, FormView
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import ugettext, ugettext_lazy as _
from forms import MakeShare
from django.core.validators import URLValidator
from myshare.models import History, MyShare
from app.forms import MakeShare, SimpleShare

class MyShareHistory(ListView):
    """implements a simple history view"""
    context_object_name = History
    model = History
    
class MyShares(ListView):
    """implements a list of all shares"""
    context_object_name = MyShare
    model = MyShare

def home(request):
    """Implements home page view"""
    return render(request, 'home.html', {'title':_("Example App Home")})

@csrf_exempt    
def example_api(request):
    """Implements a simple api for the bookmarket"""
    if request.method == "POST":
        form = MakeShare(request.POST)
        if form.is_valid():
            d = form.cleaned_data
            print d
            # need to actually do the save here.
            share.save()
    else:
        form = MakeShare()
    return render(request, 'share.html', 
                  {'title':_("Create Share"),'form':form})

@csrf_exempt
def simple_share(request):
    """implements the simple share dialog"""
    if request.method == "POST":
        form = SimpleShare(request.POST)
        if form.is_valid():
            share=MyShare()
                
            share.save()
    else:
        form = SimpleShare()
    return render(request, 'share.html', 
                  {'title':_("Create Share"), 
                   'networks':('twitter','facebook','linkedin'), 
                   'form':form})
    
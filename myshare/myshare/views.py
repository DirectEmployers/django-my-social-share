"""
views.py -- Implements UI for django-my-social-share app
"""

from django.shortcuts import render_to_response, render
from django.views.generic import DetailView, ListView, FormView
from django.http import HttpResponseRedirect, HttpResponseForbidden, Http404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.utils.translation import ugettext, ugettext_lazy as _
from myshare.models import History, MyShare, Networks
from myshare.helpers import get_share_settings

# Simple class based generic views for lists.

class MyShareHistory(ListView):
    """implements a simple history view"""
    context_object_name = History
    model = History
    
class MyShares(ListView):
    """implements a list of all shares"""
    context_object_name = MyShare
    model = MyShare
    

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
    """implements a simple sharing dialog.
    """

    if request.method == "POST":
        form = SimpleShare(request.POST)
        if form.is_valid():
            share=MyShare(user=request.user, 
                          title=form.cleaned_data['title'],
                          tweet=form.cleaned_data['tweet'],
                          description=form.cleaned_data['description'],
                          )
            
            
            # Do the Share
            for network in form.cleaned_data['networks']:
                
            share.save()
    else:
        form = SimpleShare()
    return render(request, 'share.html', 
                  {'title':_("Create Share"), 
                   'networks':('twitter','facebook','linkedin'), 
                   'form':form})




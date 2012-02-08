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

# Don't put this on the internet without restricting access unless you want
# to be phish/spam/scam central
# @login_required
def create_share (request, share_me_url=""):
    """implements a quick share me url"""
    if request.method == "GET":
        # Display a share model form 
     pass
 
def new(request, url):
    """Implements create share view
    
    Not Authenticated -- shows MYSHARE_PROMO_URL
    Authenticated -- creates a share
    """
    
    # Data Posted From Form
    if request.method == "POST":
        form = Share(request.POST)
        if form.is_valid():
            # Time to make a share
            
            return response
        else:
            # set the defaults for sharing 
            defaults = get_share_defaults()
            # set the default URL
            defaults['url'] = url
            form = Share(defaults)
            return 
    if request.method == "GET":
        # Validate the GET stuff and show the user the form.
        pass
    if request.user.is_authenticated():
        render_to_response('share_anonymous.html', RequestContext(request))
    else:
        render_to_response('share_authenticated.html', RequestContext(request))

def message(request):
    """Implements view when email/save is clicked"""
    if request.user.is_authenticated():
        # Logged in users get a much more simple sharing form
        render_to_response('email_authenticated.html', RequestContext(request))
    else:
        # Not logged in, you get invited to join and can only send to one email.
        render_to_response('email_anonymous.html', RequestContext(request))        
            
def save(request):
    """Implements save share to history for logged in users."""
    if request.user.is_authenticated():
        render_to_response('save.html', RequestContext(request))
    else:
        message = _('You must be logged in to save.')
    

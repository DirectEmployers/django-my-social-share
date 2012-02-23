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
from myshare.models import History, MyShare, Networks
from app.forms import MakeShare, SimpleShare



def home(request):
    """Implements home page view"""
    return render(request, 'home.html', {'title':_("Example App Home")})


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

    
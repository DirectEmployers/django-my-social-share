"""
views.py -- Implements UI for django-my-social-share app
"""

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponseForbidden, Http404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.utils.translation import ugettext, ugettext_lazy as _


def index(request):
    """Implements home page view"""
    pass

def share_button_clicked(request):
    """Implements view when share button is clicked
    
    Not Authenticated -- shows anonymous sharing options.
    Authenticated -- shows API share options.
    """
    if request.user.is_authenticated():
        render_to_response('share_not_authenticated.html', RequestContext(request))
    else:
        render_to_response('share_authenticated.html', RequestContext(request))

def email_button_clicked(request):
    """Implements view when email/save is clicked"""
    if request.user.is_authenticated():
        # Logged in users get a much more simple sharing form
    else:
        # Not logged in, you get invited to join and can only send to one email.
        
       

def share_not_authenticated(request):
    """Implements instant share box for anonymous users
    
    displays template that contains social share links. See template tags for
    how sharing tags are implemeted. 
    """    

    render_to_response('anonymous_share.html')

@login_required()
def share_authenticated(request):
    """Implements instant share box for authenticated users
    
    Requires django social auth be installed to work. If social auth is not 
    installed shows the anonymous sharing box
    """

    if 'django_social_auth' in settings.INSTALLED_APPS:
        # import the stuff we need
        from 
        # puth the awesome in here 
        pass
    else:
        render_to_response('anonymous_share.html')


def direct_message(request):
    """Implements send a direct message for logged in users"""
    pass

def email_share(request):
    """Implements send to a friend/self functionality"""
    pass

def save(request):
    """Implements save share to history."""
    pass

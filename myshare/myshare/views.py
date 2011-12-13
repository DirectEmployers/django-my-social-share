"""
views.py -- Implements UI for django-my-social-share app
"""

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponseForbidden, Http404
from django.template import RequestContext
from django.utils.translation import ugettext, ugettext_lazy as _


def index(request):
    """Implements home page view"""
    pass

def anonymous_share(request):
    """Implements generic social sharing with suport for MyURLs"""
    pass

def instant_share(request):
    """Implements instant share box for logged in users"""
    pass

def direct_message(request):
    """Implements send a direct message for logged in users"""
    pass

def email_share(request):
    """Implements send to a friend/self functionality"""
    pass

def save(request):
    """Implements save share to history."""
    pass

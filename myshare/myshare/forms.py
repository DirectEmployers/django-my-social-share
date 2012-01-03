"""
forms.py -- implements forms for my social share
"""

from django.forms import ModelForm
from myshare.models import Share

class EmailSaveFormAuthenticated(ModelForm):
    """Implements email form where user can customize the message
    
    Allows user to choose to save what is being shared in their personal history
    as well."""
    
    class Meta:
        Model = Share

class DirectShareForm(ModelForm):
    """Implements direct (api) sharing form
    
    This form allows the user to enter a share and select one or more networks
    to share to. Requires django-socialauth
    """
    
    class Meta:
        Model = Share

class EmailSaveFormNotAuthenticated(ModelForm):
    """Implements anonymous email form without user customization"""
    
    class Meta:
        Model = Share
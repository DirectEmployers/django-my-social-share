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

class ShareForm(ModelForm):
    """Implements sharing form
    
    This form allows the user to enter a share and select one or more networks
    to share to.
    """
    
    class Meta:
        Model = Share
        exclude = ("user","site","external_site","created","to")

class MessageForm(ModelForm):
    """Implements form for sending social messages"""

    class Meta:
        Model = Share
        exclude = ("created", "user", "site", "image_url", "image_url_title", 
                   "image_url_description", "excerpt") 

class EmailMessageForm(ModelForm):
    """Implements a form for social sharing via email.
    
    Recipients are simply a list of email addresses here."""
    
    class Meta:
        Model = Share
        exclude= ("created", "user", "site", "image_url", "image_url_title",
                  "image_url_description", "excerpt")
        
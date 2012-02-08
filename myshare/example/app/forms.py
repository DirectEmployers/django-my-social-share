"""
forms.py -- Impliments a sharing form in DjangoSocialShare
"""

from django.utils.translation import ugettext_lazy as _
import django.forms as forms
from myshare.socialshare import backends

NETWORK_CHOICES = (
    ('facebook','Facebook'),
    ('linkedin','LinkedIn'),
    ('twitter','Twitter'),
    )

class SimpleShare(forms.Form):
    """Form handler for best UX social share"""    
    networks = forms.MultipleChoiceField(
            choices=NETWORK_CHOICES,
            widget=forms.MultipleHiddenInput, 
            label=_("Select Networks"))
    tweet = forms.CharField(max_length=118,label=_("Tweet"))
    title = forms.CharField(max_length=120, 
            min_length=10, label=_("Title"),
            help_text=_("The title or headline for your share"))    
    description = forms.CharField(max_length=4096, min_length=0, 
            widget=forms.Textarea, help_text=_("Long message to share.")),
    to = forms.CharField(max_length=255,label=_("To"))


class MakeShare(forms.Form):
    """Creates a social share"""
    
    networks = forms.MultipleChoiceField(
            choices=(('facebook','facebook'),
                     ('linkedin','linkedin'),
                     ('twitter','twitter'),),
            widget=forms.CheckboxSelectMultiple, label=_("Select Networks"),
            initial="twitter",required=False)    
    title = forms.CharField(max_length=120, 
            min_length=10, label=_("Title"),
            help_text=_("The title or headline for your share"))    
    excerpt = forms.CharField(max_length=200, min_length=20,
        widget=forms.Textarea, help_text=_("Shorter Share"), required=False)
    description = forms.CharField(max_length=4096, min_length=0, 
        widget=forms.Textarea, help_text=_("Long message to share."))
    url = forms.URLField()
    url_title = forms.CharField(label=_("Title of Link"), required=False)
    url_description = forms.CharField(max_length=255, min_length=0, 
                                      widget=forms.Textarea)
    image_url = forms.URLField(label=_("URL of Image"), required=False,
                               max_length=200)
    image_url_title = forms.CharField(label=_("Title of Image"), max_length=125,
                                      required=False)
    image_url_description = forms.CharField(label=_("Image Description"), required=False, max_length=4096, widget=forms.Textarea)
    private = forms.BooleanField(label=_("Make Private"))
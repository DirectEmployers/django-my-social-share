"""
forms.py -- Impliments a sharing form in DjangoSocialShare
"""

from django.utils.translation import ugettext_lazy as _
import django.forms as forms

class MakeShare(forms.Form):
    """Creates a social share"""
    networks = forms.MultipleChoiceField(
        choices=('facebook','linkedin','twitter',),
        widget=forms.CheckboxSelectMultiple, label=_("Select Networks"))
    title = forms.CharField(max_length=120, 
        min_length=10, label=_("Title"),
        help_text=_("The title or headline for your share"))
    excerpt = forms.CharField(max_length=200, min_length=20,
        widget=forms.Textarea, help_text=_("Shorter Share"))
    description = forms.CharField(max_length=4096, min_length=0, 
        widget=forms.Textarea, help_text=_("Long message to share."))
    url = forms.URLField()
    url_title = forms.CharField()
    url_description = forms.CharField(max_length=255, min_length=0, 
                                      widget=forms.Textarea)
    image_url = forms.URLField()
    image_url_title = forms.CharField(max_length=125)
    image_url_description = forms.CharField(max_length=4096, widget=forms.Textarea)
    private = forms.BooleanField(label=_("Make Private"),
        help_text=_("Make this share private"))
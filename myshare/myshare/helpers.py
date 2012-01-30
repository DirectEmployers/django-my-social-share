"""
helpers.py -- a few convenient functions for django-my-social-share
"""
from django.conf import settings

def get_share_settings():
    result = {
              'image_url': settings.MYSHARE_DEFAULT_IMAGE_URL,
              'image_url_title': settings.MYSHARE_DEFAULT_URL_TITLE,
              'image_url_description': settings.MYSHARE_DEFAULT_URL_DESCRIPTION,
              'privacy': settings.MYSHARE_DEFAULT_PRIVACY,
              }
           
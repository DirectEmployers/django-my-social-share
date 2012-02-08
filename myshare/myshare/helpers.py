"""
helpers.py -- a few convenient functions for django-my-social-share
"""
from django.conf import settings
from BeautifulSoup import BeautifulSoup
from requests import get
from requests.exceptions import ConnectionError

def get_share_settings():
    result = {
              'image_url': settings.MYSHARE_DEFAULT_IMAGE_URL,
              'image_url_title': settings.MYSHARE_DEFAULT_URL_TITLE,
              'image_url_description': settings.MYSHARE_DEFAULT_URL_DESCRIPTION,
              'privacy': settings.MYSHARE_DEFAULT_PRIVACY,
              }

def get_headers_from_site(url):
    """Returns a dict containing the title and description of a site"""
    
    result = {'title':None,'description':None}
    try:
        soup = BeautifulSoup(get(url).content)
    except (ValueError, ConnectionError):
        return result 
    # grab <title>
    try:
        result['title'] = soup.title.string
    except (AttributeError):
        result['title'] = None
    # grab <meta name="description">
    try:
        result['description'] = soup.findAll('meta', {'name':'description'}
                                             )[0].attrMap['content']
    except (IndexError):
        result['description'] = None
    return result

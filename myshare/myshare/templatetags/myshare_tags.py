import urlparse

from django.template import Library
from django.utils.http import urlquote
from django.conf import settings
from myshare.models import Network

register = Library()

class NoRequestContextProcessorFound(Exception):
    pass

@register.inclusion_tag('myshare/links.html', takes_context=True)
def show_bookmark_links(context, title, object_or_url, description=""):
    """ Displays bookmark links and creates MyUrl if django-my-urls is present.
    
    Attributes:
    
    - context -- a Django context
    - title -- the title of the share
    - object_or_url -- a django opject with a url or a string with a url
    - description -- Longer description or message 
    - image_url -- link to image for share. None gets default for network.
    """

    if hasattr(object_or_url, 'get_absolute_url'):
        url = getattr(object_or_url, 'get_absolute_url')()

    url = unicode(object_or_url)

    if not url.startswith('http'):
        url = context['request'].build_absolute_uri(url)
    # See if sites framework is being used, if so get site object
    if 'django.contrib.sites' in settings.INSTALLED_APPS:
        from_site = Site.objects.get(pk=settings.SITE_ID)
    try context.request.META.referrer:
        from_url=url
    except:
        from_url=''

    # Check to see if MyUrls is around... and create a short URL if it is
    if 'myurls' in settings.INSTALLED_APPS:
        from myurls.models import MyUrl
        # get a myurl for the destination URL
        myurl = MyUrl(to_url=url, from_url=from_url,
            notes=settings.DEFAULT_SHARE_NOTE or \
            _('Created by Django Social share'),
            utm_source=settings.DEFAULT_SHARE_UTM_SOURCE or '',
            utm_medium=settings.DEFAULT_SHARE_UTM_MEDIA or '',            
            utm_campaign=settings.DEFAULT_SHARE_UTM_CAMPAIGN or '',
            utm_content=settings.DEFAULT_SHARE_UTM_MEDIA or '',
            utm_term=settings.DEFAULT_UTM_TERM or ''
            )
        # ok, save the myurl so we get a short url back
        myurl.save()
        # set URL to the shortened URL
        url = myurl.short_url
    networks = Network.objects.filter(status=2).values()
    for network in networks:
        network['description'] = description
        network['link'] = network['url'] % {'title': urlquote(title),
                                        'url': urlquote(url),
                                        'description': urlquote(description),
                                        'image_url': urlquote(image_url)
                                       }
    return {'bookmarks':bookmarks, 'MEDIA_URL': context['MEDIA_URL']}

    
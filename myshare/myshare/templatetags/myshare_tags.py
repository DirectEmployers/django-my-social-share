import urlparse

from django.template import Library
from django.utils.http import urlquote
from django.conf import settings
from myshare.models import Network

register = Library()

class NoRequestContextProcessorFound(Exception):
    pass

@register.inclusion_tag('myshare/links.html', takes_context=True)
def show_bookmarks(context, title, object_or_url, description=""):
    """ Displays bookmark links and creates MyUrl if django-my-urls is present.
    
    Attributes:
    
    - context -- a Django context
    - title -- the title of the share
    - object_or_url -- a django opject with a url or a string with a url
    - description -- Longer description or message 
    - image_url -- link to image for share. None results in default for network.
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
        pass


           - to_url -- the destination URL
           - notes -- user notes
           - created -- creation timestamp
           - utm_source -- Google analytics source
           - utm_medium -- Google analytics medium
           - utm_term -- Google analytics search keyword
           - utm_content -- Google analytics content
           - utm_campaign -- Google analytics campaign

    # Check to see if MyUrls is around... and create a short URL if it is
    if 'myurls' in settings.INSTALLED_APPS:
        from myurls.models import MyUrl
        # get a myurl for the destination URL
        myurl = MyUrl(to_url=url,
            notes=settings.DEFAULT_SHARE_NOTE or \
            _('Created by Django Social share'),
            utm_source=settings.DEFAULT_SHARE_UTM_SOURCE or 'socialshare',
            utm_medium=settings.DEFAULT_SHARE_UTM_MEDIA or 'socialmedia',
            
            )
    

        # since we want to share shortened URL

        url = myurl

    # TODO: Bookmark should have a .active manager:
    bookmarks = Bookmark.objects.filter(status=2).values()

    for bookmark in bookmarks:
        bookmark['description'] = description
        bookmark['link'] = bookmark['url'] % {'title': urlquote(title),
                                        'url': urlquote(url),
                                        'description': urlquote(description)
                                       }


    return {'bookmarks':bookmarks, 'MEDIA_URL': context['MEDIA_URL']}
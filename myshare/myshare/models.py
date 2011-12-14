"""
models.py -- implements models for My Social Share App
"""

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

NETWORK_SHARE_URL_HELP = _("""The URL of the network URL with codes %(url)s, 
    %(title)s, %(description)s,%(image)s and %(message)s source codes
    
    """)
                           
STATUS_CHOICES = (
    (1, 'Inactive'),
    (2, 'Active'),
)

class Network(models.Model):
    """ Stores network definitions for social networks.
    
    Allows admin to define and manage social networks using Django Admin.
    
    Attributes:
    
    - name -- name of social network
    - short_name -- max 12 character name, icon name must be short_name.png
    - share_url -- the URL used to share links
    - message_url -- the URL used for sending messages on the social network
    - image_url -- URL of image to ALWAYS provide to this network.
    - active -- Indicates if network should be shown.
    - auth_required -- Indicates if user has to be authendicated with network
    """
    
    name = models.CharField(_('Name of Social Network'), max_length=40,
        help_text=_('The name of the social network. Eg. Facebook, LinkedIn'))
    short_name = models.CharField(_('Short Name for Network'), max_length=12,
        help_text=_('Short identifier for network with no space.'))
    share_url = models.CharField(_('Share URL'), max_length=400, blank=True, 
        null=True, help_text=NETWORK_SHARE_URL_HELP)
    messaging_url = models.CharField(_('Messaging URL'), max_length=400, 
        blank=True, null=True,
        help_text=_('URL with %url, %title, and %message source codes'))
    image_url = models.URLField(_('URL of image'), null=True, blank=True,
        help_text=_('Default picture for shares to this network'))
    status = models.IntegerField(_('Active'), choices=STATUS_CHOICES,
                                 default=2)
    auth_required = models.BooleanField(_('Authentication Required'),
        help_text=_('Users must be logged in to the network to see'))
    
    def __unicode__(self):
        return u'%s (%s)' % self.name, self.short_name
    
        
class Share(models.Model):
    """Keeps sharing history
    
    Attributes:
    
    - user -- user who created the link
    - site -- django sites framework object
    - external_site -- URL for external website
    - created -- datestamp for share
    - network -- network shared on.
    - url -- Link shared
    - myurl -- MyUrl- use to track link click metrics
    - title -- Title of share (where appropriate)
    - excerpt -- Excerpt or description text shared
    - message -- Message text
    - image -- URL of image shared
    """
    
    user = models.ForeignKey(User, null=True, blank=True, 
        help_text=_('User who created share'))
    site = models.ForeignKey(Site, null=True, blank=True)
    external_site = models.URLField(_('External Site'), max_length=100, 
                                      null=True, blank=True)
    created = models.DateTimeField(_('Created'), auto_now_add=True)
    network = models.ForeignKey(_('Network'), related_name="Social Shares", 
        help_text=_('Network share was made on.'))
    url = models.URLField(_('Shared URL'), max_length=400, 
        help_text=_('Link that was shared.'))
    title = models.CharField(_('Title Text'), max_length=128, null=True,
                             blank=True)
    excerpt = models.CharField(_('Excerpt Text'), max_length=400, null=True,
        blank=True, help_text=_('Text supplied to network with share'))
    message = models.TextField(_('Message Text'), null=True, blank=True,
        help_text=_('Message text shared.'))
    image = models.URLField(_('Image Shared'), max_length=400, null=True,
        blank=True, help_text=_('URL of image shared'))
    
    def __unicode__(self):
        return u'%s (%s)' % self.network.name, self.excerpt 
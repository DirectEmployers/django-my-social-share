"""
models.py -- implements models for My Social Share App
"""
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
import socialshare

PRIVACY_CHOICES = (
    (1, 'Private'),
    (2, 'Public'),
    )

STATUS_CHOICES = (
    (30, 'Scheduled for future share'), 
    (200, 'OK - Shared'), # Shared
    (201, 'Incomplete - Conent not complete'), # Created
    (202, 'Accepted - Approved, but not shared'), # Accepted for processing
    (400, 'Bad Request'), # Failed API sharte
    (403, 'Oauth Consumer Key Failure'), # Authentication failure
    )

NETWORKS_CHOICES = []
for net in socialshare.backends.keys():
    NETWORKS_CHOICES.append((net,net,))

class Networks(models.Model):
    """Manages available list of networks.
    
    Attributes:
     - name -- Name of network (all lowercase, no spaces)
    """
    name = models.CharField(_("Social Network Name"), choices=NETWORKS_CHOICES,
                            max_length=28, unique=True, 
                            help_text=_("Name of social network all lowercase"))
                            
    def save(self, force_insert=False, force_update=False):
        """Saves model, forces lowercase for name"""
        #self.name.lower()
        super(Networks, self).save(force_insert, force_update)
        
        
class Share(models.Model):
    """Keeps sharing history
    
    Attributes:
    
    - user -- user who created the share
    - site -- django sites framework object
    - external_site -- URL for external website
    - created -- datestamp for share
    - url -- Link shared
    - url_title -- the title of the URL 
    - url_description -- the description of the URL
    - title -- Title of share (where appropriate)
    - excerpt -- Excerpt or description text shared
    - message -- Message text
    - image_url -- URL pointing to shared image
    - image_url_title -- title of the image
    - image_url_description -- The description of the image
    - private -- indicates if share history should be public (future)
    - to -- List of recipients
    """
    
    user = models.ForeignKey(User, null=True, blank=True, 
        help_text=_('User who created share'))
    status = models.IntegerField(_("Status"),choices=STATUS_CHOICES, 
        default=201, help_text=_("Share status"))
    site = models.ForeignKey(Site, null=True, blank=True)
    created = models.DateTimeField(_('Created'), auto_now_add=True)
    # This is used if we are not linking to an in-network site
    external_site = models.URLField(_('External Site'), max_length=100, 
        null=True, blank=True, help_text=_("Domain of external site."))
    # network should be the backend name from pysocialshare
    social_networks = models.ManyToManyField(Networks,
        related_name=_("Share to Network"))
    # Content
    title = models.CharField(_('Title Text'), max_length=128, null=True,
                             blank=True)
    excerpt = models.CharField(_('Excerpt Text'), max_length=255, null=True,
        blank=True, help_text=_('Text supplied to network with share'))
    message = models.TextField(_('Message Text'), null=True, blank=True,
        help_text=_('Message text shared.'))
    tweet = models.CharField(_("Tweet"), max_length=200, null=True, 
        blank=True, help_text=_("Short message for twitter"))
    # Shared link (this is the link to the content, even if it is a picture
    url = models.URLField(_('Shared URL'), max_length=400, 
        help_text=_('Link that was shared.'))
    url_title = models.CharField(_("URL Title"), max_length=128, null=True, 
        blank=True, help_text=_("Descriptive title for the link."))
    url_description= models.TextField(_("URL Description"), max_length=400,
        null=True, blank=True, help_text=_("Text description of the link."))
    # Shared image (this is usually a thumbnail that goes with a share)
    image_url = models.URLField(_('Image Shared'), max_length=400, null=True,
        blank=True, help_text=_('URL of image shared'))
    image_url_title = models.CharField(_("URL Title"), max_length=128, null=True, 
        blank=True, help_text=_("Descriptive title for the link."))
    image_url_description= models.TextField(_("URL Description"), max_length=400,
        null=True, blank=True, help_text=_("Text description of the link."))
    # TODO: add a few additional privacy options. hence the int instad of bool
    privacy = models.IntegerField(_('Privacy'), choices=PRIVACY_CHOICES, 
        default=1, help_text=_('Private shares are only visible to you.'))
    
    def share(self):
        """Performs social share"""
        pass
    
    def save(self, force_insert=False, force_update=False):
        """Saves model, updates self.status"""
        
        # Automatically update the status
        if self.status == 201:
            clean = len(self.title) > 40
            clean += len(self.url) > 16
            clean += len(self.image_url) > 16
            # set staus to ready to share
            if clean != False:
                self.status = 202
        super(Share, self).save(force_insert, force_update)
    
    
    def __unicode__(self):
        return u'%s (%s)' % self.title, self.url
    
class History(models.Model):
    """Records history of shares"""
    share = models.ForeignKey(Share, related_name=_("SharedContent"))
    user = models.ForeignKey(User, db_index=True)
    network = models.ForeignKey(Networks, related_name=_("On Social Network"),
                                db_index=True)
    created = models.DateTimeField(_('Created'), auto_now_add=True,
        help_text=_("Datestamp of share."),db_index=True)
    
    

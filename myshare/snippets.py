# Example Single Share on Twitter

from myshare.models import MyShare, History, Networks
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.conf import settings

headline = 'It is 2012. It should cost employers nothing to find an employee. It should cost job seekers nothing to find a job.'
tweet = headline[0:110]
excerpt= """You would think that job boards would have figured out that the jobs are just the content... not the product."""
link = 'http://directemployersfoundation.org'
share_to = 'linkedin'

m = MyShare(headline=headline, tweet= tweet, url=link, excerpt=excerpt, url_title="My.Jobs is a job search tool.")

m.save()
# set user and site
m.user = User.objects.get(pk=1)
m.site = Site.objects.get(pk=1)
# debug crap
print "Ready:", m.is_ready()
print "Custom URL:", m.has_custom_url()

## do the share
result = m.do_single_share('twitter',
                           settings.SHARE_TWITTER_CONSUMER_TOKEN,
                           settings.SHARE_TWITTER_CONSUMER_SECRET,
                           api_token=settings.SHARE_TWITTER_ACCESS_TOKEN,
                           api_secret=settings.SHARE_TWITTER_ACCESS_SECRET)

#result = m.do_single_share('facebook',
                           #settings.SHARE_FACEBOOK_CONSUMER_TOKEN,
                           #settings.SHARE_FACEBOOK_CONSUMER_SECRET,
                           #api_token=settings.SHARE_FACEBOOK_APP_ID,
                           #api_secret=settings.SHARE_FACEBOOK_API_KEY)
 
 
print result
#result = m.do_single_share('linkedin',
                           #settings.SHARE_LINKEDIN_CONSUMER_TOKEN, 
                           #settings.SHARE_LINKEDIN_CONSUMER_SECRET,
                           #api_token=settings.SHARE_LINKEDIN_API_KEY,
                           #api_secret=settings.SHARE_LINKEDIN_API_SECRET)
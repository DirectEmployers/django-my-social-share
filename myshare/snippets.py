# Example Single Share on Twitter

from myshare.models import MyShare, History, Networks
from django.conf import settings

title = 'It is 2012. It should cost employers nothing to find an employee. It should cost job seekers nothing to find a job.'
tweet = title
message = ''
link = 'http://directemployersfoundation.org'
share_to = 'twitter'

m = MyShare(title=title, tweet= tweet, url=link)
m.save()
print "Ready:", m.is_ready()
print "Custom URL:", m.has_custom_url()
m.do_single_share(share_to, 
                  settings.SHARE_TWITTER_CONSUMER_TOKEN,
                  settings.SHARE_TWITTER_CONSUMER_SECRET,
                  api_token=settings.SHARE_TWITTER_ACCESS_TOKEN,
                  api_secret=settings.SHARE_TWITTER_ACCESS_SECRET)

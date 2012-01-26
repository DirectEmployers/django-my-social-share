"""
backends.py -- implements a more universal social api that abstracts away the 
               differences between python social media APIs. The idea is to 
               make server to server interaction uber simple.  Authentication
               is *not* implemented here by design. Use this API once you have
               consumer keys for a user.
               
               Supported networks: Facebook, Twitter, LinkedIn and Debug.
               
               About the debug backend: it writes to stdio. 
"""

# Put all your keys in secret.py... and make sure you put secret.py in
# your VCS's ignore file.  
from secrets import *
    
backends ={}    
          
class ShareError(Exception):
    """Used for social share fails."""
    def __init__(self):
        return

    def __str__(self):
        print "ShareError", self.message or None    


class ShareBackend(object):
    """Social Sharing API. 
    
    To write a new backend, implement at the minimum """
    def __init__(self, api_token, api_secret, consumer_token="", 
                 consumer_secret="", message="", headline="", excerpt="", 
                 tweet="", url="", url_title="", url_description ="", 
                 image_url="", image_url_title="", image_url_description=""):
        """Constructor

        Parameters:
        api_token -- a valid oauth api token. This is your app's token.
        api_secret -- a valid oauth api secret. This is your app's secret.
        consumer_token -- optional consumer token.
        consumer_secret -- optional consumer secret.
        """
        self.api_token = api_token.strip()
        self.api_secret = api_secret.strip()
        self.consumer_token = consumer_token.strip()
        self.consumer_secret = consumer_secret.strip()
        self.to = []
        # deal with message content if we have it
        self.set_content(message, headline=headline, excerpt=excerpt, 
                         tweet=tweet, url=url, url_title=url_title,
                         url_description=url_description, 
                         image_url=image_url, image_url_title=image_url_title,
                         image_url_description=image_url_description)
    
    def set_content(self, message, headline="", excerpt="", tweet="", url="", 
                    url_title="", url_description ="", image_url="", 
                    image_url_title="", image_url_description=""):
        """Sets the content to be shared.  
        
        Parameters:
        message -- the message.
        headline -- the headline or subject for the message
        excerpt -- the excerpt or short version of the message
        tweet -- short 160 character max message
        url -- the url being shared
        url_title -- the title of the url
        url_description -- description of the URL
        image_url -- 
        
        """
        self.message = message.strip()
        # truncate at 128 characters
        self.headline = headline[0:128].strip()
        self.excerpt = excerpt.strip()
        # truncate tweet if it is too long
        self.tweet = tweet[0:160].strip()
        self.url = u'%s' % url.strip()
        self.url_title = url_title.strip()
        self.url_description = url_description.strip()
        self.image_url = u'%s' % image_url.strip()
        self.image_url_title = image_url_title.strip()
        self.image_url_description = image_url_description.strip()
        
    def share(self):
        """ Executes social network share""" 
        self._share()

    def send_message(self):
        """Sends message using social network. 

        parameters:
        to -- list of recipients in format expected by social network
        """
        # Make sure we have recipients. If not, blow up.
        if self.to == []:
            raise ShareError, "No recipients to send to."
        self._send_message()
        
    def _send_message(self):
        """Sends message: Like the goggles, does nothing."""
        pass

    def _share(self):
        """Shares. Like the goggles, does nothing."""
        pass
    
    
class DebugBackend(ShareBackend):
    """Implements sharing with stdio. stdio knows where you live.
    
    Parameters:
    api_token -- a valid oauth api token. This is your app's token.
    api_secret -- a valid oauth api secret. This is your app's secret.
    consumer_token -- optional consumer token.
    consumer_secret -- optional consumer secret.
    """

    def _share(self):
        """Does social share"""
        print "consumer token ", self.consumer_token
        print "consumer secret", self.consumer_secret
        print "headline:      ",self.headline
        print "excerpt:       ", self.excerpt or None
        print "message:       ", self.message or None
        print "url:           ", self.url or None
        print "image_url:     ", self.image_url or None        

    def _send_message(self):
        """sends message"""
        print "consumer token  ", self.consumer_token
        print "consumer secret ", self.consumer_secret
        for t in self.to:
            print "to:        ", t
        print "subject:   ",self.subject
        print "message:   ",self.message or None
        print "url:       ",self.url or None
        print "image_url: ",self.image_url or None        


register_share_backend('debug', 'DebugBackend')

class LinkedInBackend(ShareBackend):
    """Implements LinedIn Sharing using python-linkedin.

    Backend Settings:
    api_key -- Your API key (get from LinkedIn)
    api_secret -- Your API secret (get from LinkedIn)
    callback_url -- Your callback URL

    LinkedIn Specific Settings:
    visibility -- "connections_only", "anyone" (default) 
    """
    def __init__(self, callback_url="http://localhost", visibility="anyone"):
        super(LinkedinBackend, self).__init__(*args, **kwargs)
        # Handle custom parameters for backend
        self.callback_url = callback_url
        self.visibility = visibility
        # instantiate a linkedin API. 
        from linkedin import linkedin
        # First instantiate the api object.
        self.api = linkedin.LinkedIn(api_key=self.api_token, 
            api_secret=self.api_secret, callback_url='callback_url')
        # Force api to use a stored token/secret instead of getting one.
        # (Due to the way Python-LinkedIN is put together)
        self.api._access_token = self.consumer_token
        self.api._access_secret = self.consumer_secret

    def _share(self, connections_only=True):
        """Shares a URL via LinkedIn's API. No web browser required."""
        # set visibility to connections-only or something else...
        if connections_only:
            v = 'connections-only'
        else:
            v = 'everyone'
            
        result = self.api.share_update(comment=self.message, 
                                       title=self.headline,
                                       submitted_url=self.url, 
                                       submitted_image_url=self.image_url,
                                       description=self.excerpt, 
                                       visibility=v)         
        # python-linkedin doesn't do exceptions so we have to check for errors.
        if result == False:
            raise ShareError, self.api.get_error()

    def _send_message(self):
        """Implements python-linkedin send message.

        Note: to is a list of LinkedIn IDs and is truncated at 10 recipients.
        """

        # send the message with LI API
        result = self.api.send_message(subject=self.subject, 
                                       message=self.message, 
                                       ids=self.to)
        # python-linkedin doesn't do exceptions so we have to check for errors.
        if result == False:
            raise ShareError, self.api.get_error()

register_share_backend('linkedin','LinkedInBackend')

class TwitterBackend(ShareBackend):
    """Implements Tweepy API 
    
    Backends Settings:
    api_token -- a valid oauth api token. This is your app's token.
    api_secret -- a valid oauth api secret. This is your app's secret.
    consumer_token -- optional consumer token.
    consumer_secret -- optional consumer secret.

    Twitter Specific Settings:
    use_tco -- True or False, use Twitter's t.co shortner.
    """
    def __init__(self, use_tco=True):
        super(TwitterBackend, self).__init__(*args, **kwargs)
        # handle twitter custom parameters
        self.use_tco=use_tco
        # create a tweepy API
        from tweepy import API, OAuthHandler
        auth = OAuthHandler(self.consumer_token, self.consumer_secret)
        auth.set_access_token(self.api_token, self.api_secret)
        # Set up API
        api = API(auth)

    def send_message(self, use_tco = 'true'):
        """Processes and sends direct message.
        
        parameters:
        
        use_tco -- use the t.co url shortner
        """
        self.subject = subject.strip()
        self.message = message.strip()
        self.url = url.strip()       
        # Use url t.co url shortner?
        if self.tweet != '':
            self.tweet = _clean_tweet(use_tco=use_tco or False)    
        _send_message()
    
    def _send_message(self):
        """Implemets tweepy send direct message.

        Note: to is a list of Twitter IDs or Twitter usernames.
              Twitter usernames can change, Twitter IDs do not.
        """
        # Loop throught the to's
        for t in self.to:
            # Fail very silently for now.
            # TODO: Wire into python logging.
            try:
                self.api.send_direct_message(user=t, text=self.tweet)
            except:
                pass

register_share_backend('twitter','TwitterBackend')

    def _clean_tweet(self, use_tco=True):
        """Creates tweets by truncating subject at appropriate length.
        
        Length is calculated using the length of a t.co URL or the provided URL
        depending the use_tco parameter. 
        """
        
        if use_tco:
            length = 160 - 19
            tweet = u'%s %s' % self.subject[0:length], self.url
        else:
            length = 160-len(self.url)-1
            tweet = u'%s %s' % self.subject[0:length], self.url
        return tweet

    def _share(self):
        """Implements "sharing" on twitter which is exactly like tweeting.
        
        Note: Tweeting is the same as "updating your status".
        """
        
        # Fail very silently for now
        # TODO: Wire into python logging.
        try:
            self.api.update_status(status=self.tweet)
        except:
            pass
        
class FacebookBackend(ShareBackend):
    """Implements Facebook backend"""
    def __init__():
        super(FacebookBackend, self).init(*args, **kwargs)
        # Create a Facebook social graph API using facepy.     
        from facepy import GraphAPI
        self.api = facepy.GraphAPI()
        self.api.oauth_token = facebook_consumer_key

    def _share(self):
        """Implements sharing on Facebook by making wall posts."""
        # send the message
        
        response = self.api.post(path='me/feed',
                                 message=self.message,
                                 picture=self.image_url or None,
                                 link = self.url or None)
        if response is None:
            raise ShareError, "Facebook post to feed failed."

    def _send_message(self):
        """Implements send a message to a facebook user"""
        
        # Facebook accepts an array of name/id objects.
        response = self.api.post(path='/me/outbox',
                                 message = self.message,
                                 picture=self.image_url or None,
                                 link = self.url or None,
                                 to=self.to)
        if response is None:
            raise ShareError, "Facebook outbox Failure"

register_share_backend('facebook','FacebookBackend')

def register_share_backend(name, func_name):
    """Registers a new social sharing backend"""
    backends['name'] = func_name
    
class Share(object):
    """Shares a message with with multiple social media sites
    
    Works by iterating through a list of social media targets. A single message
    can be shared on multiple social sites and via multiple users specified in
    the targets dict.
    
    Parameters: 
    targets -- list of shares as follows:
               [{'backend':'network','setting':'value'},...]
               where backend is facebook, linkedin, twitter or debug and
               settings are key value pairs specific to the share 
               (including OAUTH token/secrets).
    """
    
    def __init__(self, message, targets={}, title="", excerpt="", 
                 url="", image_url=""):
        """Constructor"""
        # check that we have targets.
        if targets == {}:
            raise ShareError, "No targets specified"
        # process each target
        for t in targets:
            func = getattr(backends[t.network], __init__)
                
    def add_backend(*args, **kwargs):
        pass


if __name__ == "__main__":
# some crude tests
    s = ShareBackend()
    s.send_message("I am sending this to everyone I know", to=['me', 'you'])
    s.share("I am sharing with a universe of one.")
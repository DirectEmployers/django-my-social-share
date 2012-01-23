"""
backends.py -- implements a more universal social api that abstracts away the 
               differences between python social media APIs. The idea is to 
               make server to server interaction uber simple.  Authentication
               is *not* implemented here by design. Use this API once you have
               consumer keys for a user.
               
               Supported networks: Facebook, Twitter, LinkedIn and Debug.
               
               About the debug backend: it writes to stdio. 
"""
               
class ShareError(Exception):
    """Used for social share fails."""
    def __init__(self):
        return

    def __str__(self):
        print "ShareError", self.message or None    


class ShareBackend(object):
    """Social Sharing API. 
    
    To write a new backend, implement at the minimum """
    def __init__(self, api_token, api_secret,
                 consumer_token="", consumer_secret=""):
        """Constructor

        Parameters:
        api_token -- a valid oauth api token. This is your app's token.
        api_secret -- a valid oauth api secret. This is your app's secret.
        consumer_token -- optional consumer token.
        consumer_secret -- optional consumer secret.
        """
        self.api_token = api_token.strip()
        self.api_secret = api_secret.strip()
        self.consumer_token = consumer_token.strip() or None
        self.consumer_secret = consumer_secret.strip() or None
    
    def share(self, headline, excerpt='', message='', url='', image_url=''):
        """ Executes social network share""" 
        self.headline = headline.strip()
        self.excerpt = headline.strip() or None
        self.message = message.strip() or None
        self.url = u'%s' % url.strip() or None
        self.image_url = u'%s' % image_url.strip or None
        self._share()

    def send_message(self, subject, to=[], message='', url='', image_url=''):
        """Sends message using social network. 

        parameters:

        subject -- the subject
        to -- list of recipients in format expected by social network
        message -- the text of the message
        url -- url to include with message
        image_url -- url to image to include with message
        """
        # Tidy up
        self.to = to
        self.subject = subject.strip()
        self.message = message.strip()
        self.url = url.strip()
        self.image_url=image_url.strip() 
        # Send it.
        self._send_message()
        
    def _send_message(self):
        """Sends message: Like the goggles, does nothing."""
        pass

    def _share(self):
        """Shares. Like the goggles, does nothing."""
        pass

class DebugBackend(ShareBackend):
    """Implements sharing with stdio. stdio knows where you live."""

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


class LinkedinBackend(ShareBackend):
    """Implements LinedIn Sharing using python-linkedin.

    Backend Settings:
    api_key -- Your API key (get from LinkedIn)
    api_secret -- Your API secret (get from LinkedIn)
    callback_url -- Your callback URL
    visibility -- "connections_only", "anyone" (default) 
    """

    # instantiate a linkedin API. 
    from linkedin import linkedin
    # First instantiate the api object.
    api = linkedin.LinkedIn(api_key=self.api_token, api_secret=self.api_secret,
                            callback_url='callback_url')
    # Second, force the api to use a stored token/secret instead of getting one.
    api._access_token = self.consumer_token
    api._access_secret = self.consumer_secret

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
                                       submitted_image_url=image_url,
                                       description=excerpt, 
                                       visibility=v)         
        # python-linkedin doesn't do exceptions so we have to check for errors.
        if result == False:
            raise ShareError, api.get_error()

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
            raise ShareError, api.get_error()

class TwitterBackend(ShareBackend):
    """Implements Tweepy API 
    
    Backends Settings:
    use_tco -- True or False, use Twitter's t.co shortner.
    """

    from tweepy import API, OAuthHandler
    # Set api and consumer Oauth
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
        Note: Twitter usernames can change, Twitter IDs do not.
        """
        # Loop throught the to's
        for t in self.to:
            # Fail very silently for now.
            # TODO: Wire into python logging.
            try:
                self.api.send_direct_message(user=t, text=self.tweet)
            except:
                pass

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
    from facepy import GraphAPI
    api = GraphAPI(self.

    def _share(self):
        """Implements sharing on Facebook by making wall posts."""
        

class Share(object):
    """Universal one call shares them all"""
    # TODO: Load settings here (probably use python's init file module)
    
    def __init__(self, backends={}):

    
    def add_backend(*args **kwargs) 
    


if __name__ == "__main__":

from secret import *

# some crude tests
s = ShareBackend()
s.send_message("I am sending this to everyone I know", to=['me', 'you'])
s.share("I am sharing with a universe of one.")

    def send_message (self)

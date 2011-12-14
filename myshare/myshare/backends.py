"""
backends.py -- Backends for sharing services

There are two kinds of backends: public and direct. Public backends work 
by adding parameters to a url that is typically launched in a pop-up that 
allows the user to edit and share. Direct backends handle sending shares
directly to a social network via an API. 

- url - the URL being shared
- image_url - the image being shared (often set to a logo)
- excerpt - text excerpt for the share
- message - user's descriptive text
- tags - future implemenation

"""

class BaseShareBackend (object):
    """Base Sharing Backend"""

    def __init__(self):
        """Constructor"""
        
        
    
    
        
    
    
        
    
    
"""
views.py - implements views for django-my-social-share app
"""


class MyShareHistory(ListView):
    """implements a simple history view"""
    context_object_name = History
    model = History
    
class MyShares(ListView):
    """implements a list of all shares"""
    context_object_name = Shares
    model = Shares

def home(request):
    """Implements home page view"""
    pass

def api(request, url):
    """Implements a simple api for the bookmarket"""
    pass


    
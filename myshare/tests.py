from django.test import TestCase
from django.conf import settings
from django.contrib.sites.models import Site

from myshare.models import Networks, MyShare

class MyShareTests(TestCase):
    
    def test_network_save(self):
        network = Networks(name="BookFace")
        n.save()
        self.assertEqual('bookface', n.name)
        
    def test_share_status(self):
        """Test that share staus codes are correctly updated"""
        s = MyShare()
        # test before saving
        self.assertEqual(s.status, 201)
        # do the save
        s.save()
        # test aftermath
        self.assertEqual(s.status, 201)
        # Add a title
        s.headline="This is Dangerous"
        s.save()
        self.assertEqual(s.status, 202)
    
        
    
        
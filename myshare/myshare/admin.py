"""
admin.py -- Django admin classes for myshare
"""
from django.contrib import admin
from models import Network, Share

class NetworkOption(admin.ModelAdmin):
    """Default Network admin defs"""
    list_display=('name','short_name')
    
class ShareOption(admin.ModelAdmin):
    """Default share history admin defs"""
    list_display=('created', 'user', 'network.short_name')

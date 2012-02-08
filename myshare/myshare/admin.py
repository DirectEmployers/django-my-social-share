"""
admin.py -- Django admin classes for myshare
"""
from django.contrib import admin
from myshare.models import History, MyShare

class HistoryOption(admin.ModelAdmin):
    """Default history admin defs"""
    list_display=('name','short_name')
    
class ShareOption(admin.ModelAdmin):
    """Default share history admin defs"""
    list_display=('created', 'user', 'network.short_name')


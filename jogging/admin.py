from django.contrib import admin
from jogging.models import Log

class LogAdmin(admin.ModelAdmin):
    date_hierarchy = 'datetime' 
    model = Log
    list_display = ['datetime', 'host', 'level', 'source', 'msg']
    search_fields = ['source', 'msg', 'host']
    list_filter = ['level', 'source', 'host']

admin.site.register(Log, LogAdmin)

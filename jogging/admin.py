from django.contrib import admin
from jogging.models import Log

class LogAdmin(admin.ModelAdmin):
    date_hierarchy = 'datetime' 
    model = Log
    list_display = ['datetime', 'level', 'source', 'abbrev_msg']
    search_fields = ['source', 'msg']
    list_filter = ['level', 'source']

admin.site.register(Log, LogAdmin)

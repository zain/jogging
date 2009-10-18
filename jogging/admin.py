from django.contrib import admin
from jogging.models import Log

class LogAdmin(admin.ModelAdmin):
    model = Log
    list_display = ['datetime', 'level', 'source', 'msg']
    search_fields = ['source']
    list_filter = ['level', 'source']

admin.site.register(Log, LogAdmin)
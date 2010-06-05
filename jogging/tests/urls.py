#:coding=utf-8:
from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
    (r'exception_view', 'jogging.tests.views.exception_view'),
)

from django.db import models
import datetime

class Log(models.Model):
    datetime = models.DateTimeField(default=datetime.datetime.now)
    level = models.CharField(max_length=128)
    msg = models.TextField()
    source = models.CharField(max_length=128, blank=True)
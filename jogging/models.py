import datetime

import logging as py_logging

from django.db import models
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings


class Log(models.Model):
    "A log message, used by jogging's DatabaseHandler"
    datetime = models.DateTimeField(default=datetime.datetime.now)
    level = models.CharField(max_length=128)
    msg = models.TextField()
    source = models.CharField(max_length=128, blank=True)
    host = models.CharField(max_length=200, blank=True, null=True)

    def abbrev_msg(self, maxlen=500):
        if len(self.msg) > maxlen:
            return u'%s ...' % self.msg[:maxlen]
        return self.msg
    abbrev_msg.short_description = u'abbreviated msg'


## Set up logging handlers

def jogging_init():
    def add_handlers(logger, handlers):
        if not handlers:
            return

        for handler in handlers:
            if type(handler) is dict:
                if 'format' in handler:
                    handler['handler'].setFormatter(py_logging.Formatter(handler['format']))
                if 'level' in handler:
                    handler['handler'].setLevel(handler['level'])
                logger.addHandler(handler['handler'])
            else:
                logger.addHandler(handler)


    if hasattr(settings, 'LOGGING'):
        for module, properties in settings.LOGGING.items():
            logger = py_logging.getLogger(module)

            if 'level' in properties:
                logger.setLevel(properties['level'])
            elif hasattr(settings, 'GLOBAL_LOG_LEVEL'):
                logger.setLevel(settings.GLOBAL_LOG_LEVEL)
            elif 'handlers' in properties:
                # set the effective log level of this loger to the lowest so
                # that logging decisions will always be passed to the handlers
                logger.setLevel(1)
                pass
            else:
                raise ImproperlyConfigured(
                    "A logger in settings.LOGGING doesn't have its log level set. " +
                    "Either set a level on that logger, or set GLOBAL_LOG_LEVEL.")

            handlers = [] 
            if 'handler' in properties:
                handlers = [properties['handler']]
            elif 'handlers' in properties:
                handlers = properties['handlers']
            elif hasattr(settings, 'GLOBAL_LOG_HANDLERS'):
                handlers = settings.GLOBAL_LOG_HANDLERS

            add_handlers(logger, handlers)

    elif hasattr(settings, 'GLOBAL_LOG_LEVEL') and hasattr(settings, 'GLOBAL_LOG_HANDLERS'):
        logger = py_logging.getLogger('')
        logger.setLevel(settings.GLOBAL_LOG_LEVEL)
        handlers = settings.GLOBAL_LOG_HANDLERS

        add_handlers(logger, handlers)

jogging_init()
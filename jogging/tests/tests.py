#:coding=utf8:

import logging

from django.test import TestCase as DjangoTestCase
from django.conf import settings

from jogging.models import Log, jogging_init

class DatabaseHandlerTestCase(DjangoTestCase):
    
    def setUp(self):
        from jogging.handlers import DatabaseHandler, MockHandler
        import logging
        
        self.LOGGING = getattr(settings, 'LOGGING', None)
        
        settings.LOGGING = {
            'database_test': {
                'handler': DatabaseHandler(),
                'level': logging.DEBUG,
            },
            'multi_test': {
                'handlers': [
                    { 'handler': DatabaseHandler(), 'level': logging.DEBUG },
                    { 'handler': MockHandler(), 'level': logging.DEBUG },
                ],
            },
        }
        
        jogging_init()
    
    def tearDown(self):
        import logging

        # clear out all handlers on loggers
        loggers = [logging.getLogger(""), logging.getLogger("database_test"), logging.getLogger("multi_test")]
        for logger in loggers:
            logger.handlers = []
        
        # delete all log entries in the database
        for l in Log.objects.all():
            l.delete()
        
        if self.LOGGING:
            settings.LOGGING = self.LOGGING
        jogging_init()
    
    def test_basic(self):
        logger = logging.getLogger("database_test")
        logger.info("My Logging Test")
        log_obj = Log.objects.latest()
        self.assertEquals(log_obj.level, "INFO")
        self.assertEquals(log_obj.source, "database_test")
        self.assertEquals(log_obj.msg, "My Logging Test")
        self.assertTrue(log_obj.host)
    
    def test_multi(self):
        logger = logging.getLogger("multi_test")
        logger.info("My Logging Test")
        
        log_obj = Log.objects.latest()
        self.assertEquals(log_obj.level, "INFO")
        self.assertEquals(log_obj.source, "multi_test")
        self.assertEquals(log_obj.msg, "My Logging Test")
        self.assertTrue(log_obj.host)
        
        log_obj = settings.LOGGING["multi_test"]["handlers"][1]["handler"].msgs[0]
        self.assertEquals(log_obj.levelname, "INFO")
        self.assertEquals(log_obj.name, "multi_test")
        self.assertEquals(log_obj.msg, "My Logging Test")

class DictHandlerTestCase(DjangoTestCase):

    def setUp(self):
        from jogging.handlers import MockHandler
        import logging
        
        self.LOGGING = getattr(settings, 'LOGGING', None)

        settings.LOGGING = {
            'dict_handler_test': {
                'handlers': [
                    { 'handler': MockHandler(), 'level': logging.ERROR },
                    { 'handler': MockHandler(), 'level': logging.INFO },
                ],
            },
        }
        
        jogging_init()
    
    def tearDown(self):
        import logging

        # clear out all handlers on loggers
        loggers = [logging.getLogger(""), logging.getLogger("database_test"), logging.getLogger("multi_test")]
        for logger in loggers:
            logger.handlers = []
        
        # delete all log entries in the database
        for l in Log.objects.all():
            l.delete()
        
        if self.LOGGING:
            settings.LOGGING = self.LOGGING
        jogging_init()
    
    def test_basic(self):
        logger = logging.getLogger("dict_handler_test")
        error_handler = settings.LOGGING["dict_handler_test"]["handlers"][0]["handler"]
        info_handler = settings.LOGGING["dict_handler_test"]["handlers"][1]["handler"]


        logger.info("My Logging Test")
        # Make sure we didn't log to the error handler
        self.assertEquals(len(error_handler.msgs), 0)

        log_obj = info_handler.msgs[0]
        self.assertEquals(log_obj.levelname, "INFO")
        self.assertEquals(log_obj.name, "dict_handler_test")
        self.assertEquals(log_obj.msg, "My Logging Test")

class GlobalExceptionTestCase(DjangoTestCase):
    urls = 'jogging.tests.urls'
    
    def setUp(self):
        from jogging.handlers import DatabaseHandler, MockHandler
        import logging
        
        self.LOGGING = getattr(settings, 'LOGGING', None)
        self.GLOBAL_LOG_HANDLERS = getattr(settings, 'GLOBAL_LOG_HANDLERS', None)
        self.GLOBAL_LOG_LEVEL = getattr(settings, 'GLOBAL_LOG_LEVEL', None)
        
        loggers = [logging.getLogger("")]
        for logger in loggers:
            logger.handlers = []
        
        settings.LOGGING = {}
        settings.GLOBAL_LOG_HANDLERS = [MockHandler()]
        settings.GLOBAL_LOG_LEVEL = logging.DEBUG
        
        jogging_init()
    
    def tearDown(self):
        import logging

        # clear out all handlers on loggers
        loggers = [logging.getLogger("")]
        for logger in loggers:
            logger.handlers = []
        
        # delete all log entries in the database
        for l in Log.objects.all():
            l.delete()
        
        if self.LOGGING:
            settings.LOGGING = self.LOGGING
        if self.GLOBAL_LOG_HANDLERS:
            settings.GLOBAL_LOG_HANDLERS = self.GLOBAL_LOG_HANDLERS
        if self.GLOBAL_LOG_LEVEL:
            settings.GLOBAL_LOG_LEVEL = self.GLOBAL_LOG_LEVEL
        jogging_init()
 
    def test_exception(self):
        from views import TestException
        try:
            resp = self.client.get("/exception_view")
            self.fail("Expected Exception")
        except TestException:
            pass
        root_handler = logging.getLogger("").handlers[0]

        log_obj = root_handler.msgs[0]
        self.assertEquals(log_obj.levelname, "ERROR")
        self.assertEquals(log_obj.name, "root")
        self.assertTrue("Traceback" in log_obj.msg)

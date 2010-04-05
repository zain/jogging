import logging as py_logging
import sys

class LoggingWrapper(object):
    LOGGING_LEVELS = {
        'debug': py_logging.DEBUG,
        'info': py_logging.INFO,
        'warning': py_logging.WARNING,
        'error': py_logging.ERROR,
        'critical': py_logging.CRITICAL
    }
    
    def debug(self, msg, *args, **kwargs):
        caller = sys._getframe(1).f_globals['__name__']
        self.log('debug', msg, caller, *args, **kwargs)
    
    def info(self, msg, *args, **kwargs):
        caller = sys._getframe(1).f_globals['__name__']
        self.log('info', msg, caller, *args, **kwargs)
    
    def warning(self, msg, *args, **kwargs):
        caller = sys._getframe(1).f_globals['__name__']
        self.log('warning', msg, caller, *args, **kwargs)
    
    def error(self, msg, *args, **kwargs):
        caller = sys._getframe(1).f_globals['__name__']
        self.log('error', msg, caller, *args, **kwargs)
    
    def critical(self, msg, *args, **kwargs):
        caller = sys._getframe(1).f_globals['__name__']
        self.log('critical', msg, caller, *args, **kwargs)
    
    def exception(self, msg='', exception=None, request=None, *args, **kwargs):
        import traceback, sys
        
        if exception:
            tb = ''.join(traceback.format_exception(sys.exc_info()[0],
                sys.exc_info()[1], sys.exc_info()[2]))
        else:
            tb = ''
        
        if request:
            source = request.build_absolute_uri()
        else:
            source = 'Exception'
        
        self.log('error', msg + tb, source, *args, **kwargs)
    
    def log(self, level, msg, source=None, *args, **kwargs):
        import sys
        
        if not source:
            source = sys._getframe(1).f_globals['__name__']

        logger = self.get_logger(source)
        kwargs.update(source=source)
        
        if sys.version_info >= (2, 5):
            logger.log(self.LOGGING_LEVELS[level], msg, *args, **{'extra': kwargs})
        else:
            logger.log(self.LOGGING_LEVELS[level], msg, *args, **kwargs)
    
    def get_logger(self, source):
        from django.conf import settings
        
        chunks = source.split('.')
        modules = ['.'.join(chunks[0:n]) for n in range(1, len(chunks) + 1)]
        modules.reverse()
        
        if hasattr(settings, 'LOGGING'):
            for source in modules:
                if source in settings.LOGGING:
                    return py_logging.getLogger(source)
        
        return py_logging.getLogger('') # root logger

logging = LoggingWrapper()
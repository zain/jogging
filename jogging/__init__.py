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
        from django.utils.encoding import iri_to_uri

        if exception:
            tb = ''.join(traceback.format_exception(sys.exc_info()[0],
                sys.exc_info()[1], sys.exc_info()[2]))
        else:
            tb = ''

        if request:
            location = '%s://%s%s' % (request.is_secure() and 'https' or 'http',
                                      request.get_host(), request.path)
            source = iri_to_uri(location)
            absolute_uri = request.build_absolute_uri()
            try:
                request_repr = repr(request)
            except:
                request_repr = "Request repr() unavailable"
            message = """Absolute URI: %s
========================================
%s%s
========================================
Request:
%s""" % (absolute_uri, msg, tb, request_repr)
        else:
            source = 'Exception'
            message = "%s%s" % (msg, tb)

        self.log('error', message, source, *args, **kwargs)

    def log(self, level, msg, source=None, *args, **kwargs):
        import sys
        
        if not source:
            source = sys._getframe(1).f_globals['__name__']

        logger = self.get_logger(source)

        
        if sys.version_info >= (2, 5):
            kwargs.update(source=source)
            logger.log(level=self.LOGGING_LEVELS[level], msg=msg, extra=kwargs, *args)
        else:
            logger.log(level=self.LOGGING_LEVELS[level], msg=msg, *args, **kwargs)
    
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

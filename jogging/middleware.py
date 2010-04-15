class LoggingMiddleware(object):    
    def process_exception(self, request, exception):
        from jogging import logging
        logging.exception(exception=exception, request=request)

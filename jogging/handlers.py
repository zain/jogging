import datetime, logging

class NullHandler(logging.Handler):
    def emit(self, record):
        pass

class DatabaseHandler(logging.Handler):
    def emit(self, record):
        from jogging.models import Log
        
        if hasattr(record, 'source'):
            source = record.source
        else:
            source = record.name
        
        Log.objects.create(source=source, level=record.levelname, msg=record.msg)
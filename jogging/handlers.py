import datetime, logging

class DatabaseHandler(logging.Handler):
    def emit(self, record):
        from jogging.models import Log
        Log.objects.create(source=record.source, level=record.levelname, msg=record.msg)
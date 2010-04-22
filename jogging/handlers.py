import datetime, logging
import os

HOST = os.uname()[1]

class NullHandler(logging.Handler):
    def emit(self, record):
        pass

class MockHandler(logging.Handler):
    def __init__(self, *args, **kwargs):
        self.msgs = []
        logging.Handler.__init__(self, *args, **kwargs)

    def emit(self, record):
        self.msgs.append(record)

class DatabaseHandler(logging.Handler):
    def emit(self, record):
        from jogging.models import Log
        
        if hasattr(record, 'source'):
            source = record.source
        else:
            source = record.name
        
        Log.objects.create(source=source, level=record.levelname, msg=record.msg, host=HOST)

class EmailHandler(logging.Handler):
    def __init__(self, from_email=None, recipient_spec=None, fail_silently=False, auth_user=None, auth_password=None, *args, **kwargs):
        logging.Handler.__init__(self, *args, **kwargs)
        self.recipient_spec = recipient_spec or () 
        self.from_email = from_email
        self.auth_user = auth_user
        self.auth_password = auth_password
        self.fail_silently = fail_silently

    def emit(self, record):
        from django.conf import settings
        from django.core.mail import send_mail 

        if hasattr(record, 'source'):
            source - record.source
        else:
            source = record.name

        send_mail(
            subject="%s[%s] %s: %s" % (settings.EMAIL_SUBJECT_PREFIX, HOST, source, record.levelname.upper()),
            message=record.msg,
            from_email=self.from_email or settings.SERVER_EMAIL,
            recipient_list=[a[1] for a in (self.recipient_spec or settings.ADMINS)],
            fail_silently=self.fail_silently,
            auth_user=self.auth_user,
            auth_password=self.auth_password,
        )

Jogging is a thin wrapper around Python's logging functionality to make Django logging easier. 

With Jogging, you can control the destination, format, and verbosity of logs at any level. Configuring module-level logging is just as easy as for specific functions.

To use it, you add a few configurations to settings.py, import Jogging's log module instead of Python's, and then log away like you normally do. 

Python's logging module does all the heavy lifting. As a result, you can use Jogging to configure logging for existing code. And great care has been taken to make sure logging's power isn't hidden.

This isn't production ready yet, but it will be soon. Feedback appreciated!

===========
Install
===========
1. Add 'jogging' to your INSTALLED_APPS
2. Add 'jogging.middleware.LoggingMiddleware' to your MIDDLEWARE_CLASSES

===========
Configure
===========
Code samples are easier than words, so here's a few of them. These go in settings.py.

Basic
--------

::

    from jogging.handlers import DatabaseHandler
    import logging

    GLOBAL_LOG_LEVEL = logging.INFO
    GLOBAL_LOG_HANDLERS = [DatabaseHandler()] # takes any Handler object that Python's logging takes

Everything INFO and above will get logged to the database.

Note that Jogging doesn't wrap Handlers; they're the same as in logging. This means you can do all the fancy schmancy things logger's Handlers let you do, and then throw the Handler objects into Jogger.


Intermediate
----------------

::

    from jogging.handlers import DatabaseHandler
    from logging.handlers import StreamHandler
    import logging

    LOGGING = {
        # all logs from myapp1 go to the database
        'myapp1': {
            'handler': DatabaseHandler(), # an initialized handler object
            'level': logging.DEBUG,
        },
    
        # ...except for this one view which will log CRITICAL to stderr
        'myapp1.views.super_important_view': {
            'handler': StreamHandler(),
            'level': logging.CRITICAL,
        },
    }

Only the most specific logger will be matched (i.e. myapp1.views.super_important_view won't be logged to the database in this example).


Advanced
----------------

::

    from jogging.handlers import DatabaseHandler
    from logging.handlers import StreamHandler, FileHandler
    import logging

    LOGGING = {
        # all logs from myapp1 go to the database
        'myapp1': {
            'handler': DatabaseHandler(),
            'level': logging.DEBUG,
        },
    
        # this time, we'll have super_important_view log CRITICAL to stderr again, but
        # we'll also have it log everything to the database
        'myapp1.views.super_important_view': {
            'handlers': [
                { 'handler': StreamHandler(), 'level': logging.CRITICAL, 
                    'format': "%(asctime)-15s %(source): %(message)s %(foo)s" },
                { 'handler': DatabaseHandler(), 'level': logging.DEBUG },
            ]
        },
    
        # this is the name of a logger that a third party app already logs to. 
        # you can configure it just like the others, without breaking anything.
        'simple_example': {
            'handler': StreamHandler(),
            'level': logging.CRITICAL,
        }
    }

The format property on handlers takes the same specifiers as Python's logging, plus some extras:
- "%(source)s" is the method that made the logging call.
- "%(foo)" is a parameter passed into the logging call.

===========
Usage
===========

::

    from jogging import logging
    logging.info("I'm an info message")
    logging.debug(msg="I'm a debug message", foo="bar")

Remember "%(foo)s" from the 'format' property in the Advanced configuration above? It will be populated with "bar" in the debug call. 

======================
Custom Handlers
======================
jogging.handlers.DatabaseHandler
  Logs to the database, so logs are browsable/searchable/filterable in the admin.

jogging.handlers.EmailHandler
  Coming soon. Logs to emails.

jogging.handlers.InlineOnPageHandler
  Coming soon. Append logs to the bottom of the rendered page.

======================
Implementation
======================
Much inspiration was taken from Django's logging proposal:
http://groups.google.com/group/django-developers/browse_thread/thread/8551ecdb7412ab22

Jogging requires a dictionary, settings.LOGGING, that defines the loggers you want to control through Jogging (by name). Here is how Jogging works:

1. All loggers are created on server startup from settings.LOGGING (that code is in the middleware's __init__ function, for lack of a better place). Handlers are added to the loggers as defined, and levels are set.
2. When your app calls Jogging's log functions, the calling function is matched against the logger names in settings.LOGGING and the most specific logger is chosen. For example, say myproj.myapp.views.func is the caller; it will match loggers named "myproj.myapp.views.func", "myproj.myapp.views", "myproj.myapp", and "myproj". The earliest one that matches will be chosen.
3. log() is called on the chosen logger, and Python's logging module takes over from here.

===========
Resources
===========
List of handlers in Python's logging module: 
http://docs.python.org/library/logging.html#handler-objects

Format specifiers for Python's logging module:
http://docs.python.org/library/logging.html#formatter-objects

===========
ToDo
===========
- Figure out some way to instantiate handlers outside of settings.py (e.g. so the ORM can be used)
- Create more custom handlers
- Figure out how exceptions should be logged
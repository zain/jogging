#:coding=utf8:

class TestException(Exception):
    pass

def exception_view(request):
    raise TestException("This is a test exception")

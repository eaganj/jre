# Misc debugging utility functions
# Copyright (C) 2003-2009 James R. Eagan <eaganjr@acm.org>

import code
import sys
import traceback

try:
    from Foundation import NSLog
except ImportError:
    def NSLog(msg, *args):
        print msg % (args)

ENABLE_DEBUGGING = True

try:
    from functools import wraps
except ImportError:
    # Pre 2.5.  
    def wraps(wrapper, func):
        wrapper.__name__ = func.__name__
        wrapper.__doc__ = func.__doc__
        wrapper.__dict__ = func.__dict__
        return wrapper

def TRACE_STR(howFarBack=0):
    fo = sys._getframe(howFarBack+1)
    co = fo.f_code
    fileName = co.co_filename
    # Replace some common pathnames with their canonical versions
    if fileName.find('..') != -1:
        fileName = os.path.abspath(fileName)
    if fileName.startswith('/private/var/automount'):
        fileName = fileName.replace('/private/var/automount', '')
    # Output the trace in Eclipse format to integrate with its hyperlinking capabilities.
    return '  File "%s", line %s, in %s' % (fileName, fo.f_lineno, co.co_name)

def TRACE(howFarBack=0, message=None):
    if ENABLE_DEBUGGING:
        #print TRACE_STR(howFarBack+1)
        if message:
            NSLog(message)
        NSLog(u"%s" % (TRACE_STR(howFarBack+1)))
    
def NOT_IMPLEMENTED(message='This feature is not currently implemented.', howFarBack=0):
    message = '%s at:\n%s' % (message, TRACE_STR(howFarBack+1).strip())
    print message

def DEPRECATED(message=u"DeprecationWarning", howFarBack=0):
    NOT_IMPLEMENTED(message, howFarBack=howFarBack+1)


# Trap exceptions functions are intended to be used as decorators to prevent exceptions
# from propogating outside the trapping method.  This is useful, e.g., to prevent python
# exceptions from propogating into an Objective-C or Java runtime.
#
# Because Objective-C does not support variable-length argument lists to methods, we use this
# convoluted mess of different trappers depending on the number of arguments to the
# trapped method.
def trap_exceptions(func):
    try:
        num_args = func.func_code.co_argcount
        return trap_exceptions_map.get(num_args, trap_exceptions_any)(func)
    except:
        return trap_exceptions_any
    
def trap_exceptions_any(func):
    @wraps(func)
    def trapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except:
            sys.stderr.write('Exception in %s: ' % (func.__name__))
            traceback.print_exception(*sys.exc_info())
    return trapper

def trap_exceptions_func0(func):
    @wraps(func)
    def trapperf0():
        try:
            return func()
        except:
            sys.stderr.write('Exception in %s: ' % (func.__name__))
            traceback.print_exception(*sys.exc_info())
    return trapperf0
    
def trap_exceptions0(func):
    @wraps(func)
    def trapper0(self):
        try:
            return func(self)
        except:
            sys.stderr.write(u'Exception in %s: ' % (func.__name__))
            traceback.print_exception(*sys.exc_info())
    return trapper0

def trap_exceptions1(func):
    @wraps(func)
    def trapper_(self, arg):
        try:
            return func(self, arg)
        except:
            sys.stderr.write(u'Exception in %s: ' % (func.__name__))
            traceback.print_exception(*sys.exc_info())
    return trapper_

def trap_exceptions2(func):
    @wraps(func)
    def trapper_two_(self, arg1, arg2):
        try:
            return func(self, arg1, arg2)
        except:
            sys.stderr.write(u'Exception in %s: ' % (func.__name__))
            traceback.print_exception(*sys.exc_info())
    return trapper_two_

def trap_exceptions3(func):
    @wraps(func)
    def trapper_two_three_(self, arg1, arg2, arg3):
        try:
            return func(self, arg1, arg2, arg3)
        except:
            sys.stderr.write(u'Exception in %s: ' % (func.__name__))
            traceback.print_exception(*sys.exc_info())
    return trapper_two_three_

def trap_exceptions4(func):
    @wraps(func)
    def trapper_two_three_four_(self, arg1, arg2, arg3, arg4):
        try:
            return func(self, arg1, arg2, arg3, arg4)
        except:
            sys.stderr.write(u'Exception in %s: ' % (func.__name__))
            traceback.print_exception(*sys.exc_info())
    return trapper_two_three_four_

def trap_exceptions5(func):
    @wraps(func)
    def trapper_two_three_four_five_(self, arg1, arg2, arg3, arg4, arg5):
        try:
            return func(self, arg1, arg2, arg3, arg4, arg5)
        except:
            sys.stderr.write(u'Exception in %s: ' % (func.__name__))
            traceback.print_exception(*sys.exc_info())
    return trapper_two_three_four_five_

trap_exceptions_map = { 0: trap_exceptions_func0,
                        1: trap_exceptions0,
                        2: trap_exceptions1,
                        3: trap_exceptions2,
                        4: trap_exceptions3,
                        5: trap_exceptions4,
                        6: trap_exceptions5,
                      }
javaentrant = trap_exceptions

def printStackTrace(message=''):
    if message:
        sys.stderr.write(message)
        sys.stderr.write('\n')
        
    traceback.print_exception(*sys.exc_info())

def interact():
    f = sys._getframe(1)
    banner = u'Python %s\n' \
             u'Type "help", "copyright", "credits" or "license" for more information.\n' \
             u'In %s line %s at %s\n' \
             u'Locals: %s' % (sys.version, f.f_code.co_filename, f.f_lineno,
                              f.f_code.co_name, u', '.join(f.f_locals.keys()))
    scope = {}
    scope.update(f.f_globals)
    scope.update(f.f_locals)
    code.interact(banner, local=scope)
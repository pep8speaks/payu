import json
import inspect
from functools import wraps

# Globals
is_dry_run = False
is_verbose = True
retval = 0

def return_value(value):
    """Set return value when dry_run is invoked """
    global retval
    retval = value

def verbose(Flag):
    """Turn on (and off) printing call arguments"""
    global is_verbose
    is_verbose = Flag

def dry_run(Flag):
    """Turn on (and off) not running subprocess, just printing out arguments"""
    global is_dry_run
    is_dry_run = Flag
    if is_dry_run: verbose(True)

def dryrunner(func):
    """
    Function decorator to add dry run checks
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if is_dry_run:
            return retval
        else:
            return func(*args, **kwargs)
    return wrapper

def verbosity(func):
    """
    Function decorator to add verbose output
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if is_verbose:
            filename, linenum, routine = get_caller()
            print(json.dumps([ filename, linenum, routine, func.__name__, args, kwargs ] ))
        return func(*args, **kwargs)
    return wrapper

def debugger(func):
    """
    Function decorator to add verbose output and dry run checks
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if is_verbose:
            filename, linenum, routine = get_caller()
            print(json.dumps([ filename, linenum, routine, func.__name__, args, kwargs ] ))
        if is_dry_run:
            return retval
        else:
            return func(*args, **kwargs)
    return wrapper

def get_caller():
    """
    Grab the 3rd frame in outerframes (first is frame is get_caller, second frame
    the frame of the routine we're intercepting), and return file name, line number
    and routine name
    """
    frame = inspect.getouterframes(inspect.currentframe())[2]
    return frame[1:4]

def dumpvars(*args, **kwargs):
    """Print JSON serialised representations"""
    filename, linenum, routine = get_caller()
    print(json.dumps({ filename : { linenum : [ routine, args, kwargs ] } }))

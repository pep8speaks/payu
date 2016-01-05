
from subprocess import *

# Globals
is_dry_run = False
is_verbose = False
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

# Save original routines
check_output_orig = check_output
call_orig = call

# Create wrappers around original routines
def check_output(*popenargs, **kwargs):
    if is_verbose:
        print "subprocess.check_output :: ",popenargs, kwargs
    if is_dry_run:
        return retval
    else:
        return check_output_orig(*popenargs, **kwargs)
 
def call(*popenargs, **kwargs):
    if is_verbose:
        print "subprocess.call :: ",popenargs, kwargs
    if is_dry_run:
        return retval
    else:
        return call_orig(*popenargs, **kwargs)   

import subprocess
from payu.debug import debugger

@debugger
def check_output(*args, **kwargs):
    return subprocess.check_output(*args, **kwargs)

@debugger
def check_call(*args, **kwargs):
    return subprocess.check_call(*args, **kwargs)

@debugger
def call(*args, **kwargs):
    return subprocess.call(*args, **kwargs)

# Create wrappers around original routines
## def check_output(*popenargs, **kwargs):
##     if is_verbose:
##         dump_vars(*openargs, **kwargs)
##     if is_dry_run:
##         return retval
##     else:
##         return check_output_orig(*popenargs, **kwargs)
 
## def call(*popenargs, **kwargs):
##     if is_verbose:
##         dump_vars( openargs, kwargs )
##     if is_dry_run:
##         return retval
##     else:
##         return call_orig(*popenargs, **kwargs)   

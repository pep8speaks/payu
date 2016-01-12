"""payu.os_wrapper
   ===============

   Wrap some standard os functions for debugging and testing

   :copyright: Copyright 2011-2014 Marshall Ward, see AUTHORS for details.
   :license: Apache License, Version 2.0, see LICENSE for details.
"""

# Standard library
import os
# Straight import of vars/functions that aren't wrapped
from os import listdir, environ, curdir, execl, devnull, umask, getuid, getcwd

# Local
from payu.debug import debugger

# Allow seamless access to os.path through wrapper
path = os.path

# Wrap functions which have real system side-effects
@debugger
def makedirs(*args, **kwargs):
    return os.makedirs(*args, **kwargs)

@debugger
def symlink(*args, **kwargs):
    return os.symlink(*args, **kwargs)

@debugger
def remove(*args, **kwargs):
    return os.remove(*args, **kwargs)

@debugger
def rename(*args, **kwargs):
    return os.rename(*args, **kwargs)

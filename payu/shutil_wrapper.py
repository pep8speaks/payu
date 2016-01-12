"""payu.shutils_wrapper
   ===============

   Wrap some standard shutils functions for debugging and testing

   :copyright: Copyright 2011-2014 Marshall Ward, see AUTHORS for details.
   :license: Apache License, Version 2.0, see LICENSE for details.
"""

# Standard library
import shutil

# Local
from payu.debug import debugger

@debugger
def copy(*args, **kwargs):
    return shutil.copy(*args, **kwargs)

@debugger
def move(*args, **kwargs):
    return shutil.move(*args, **kwargs)

@debugger
def rmtree(*args, **kwargs):
    return shutil.rmtree(*args, **kwargs)

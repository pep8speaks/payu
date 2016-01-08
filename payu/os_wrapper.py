import os
from payu.debug import debugger

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
def islink(*args, **kwargs):
    return os.path.islink(*args, **kwargs)

@debugger
def split(*args, **kwargs):
    return os.path.split(*args, **kwargs)

@debugger
def isabs(*args, **kwargs):
    return os.path.isabs(*args, **kwargs)

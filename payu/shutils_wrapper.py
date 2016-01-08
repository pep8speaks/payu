import shutils
from payu.debug import debugger

@debugger
def copy(*args, **kwargs):
    return shutils.copy(*args, **kwargs)

@debugger
def move(*args, **kwargs):
    return shutils.move(*args, **kwargs)

@debugger
def rmtree(*args, **kwargs):
    return shutils.rmtree(*args, **kwargs)

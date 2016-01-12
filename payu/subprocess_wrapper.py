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

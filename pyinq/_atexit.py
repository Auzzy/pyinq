import atexit

_exitfuncs = {}

def register(func, *args, **kwargs):
	_exitfuncs[func] = (args,kwargs)

def unregister(func):
	if func in _exitfuncs:
		del _exitfuncs[func] 

def _run_at_exit():
	for func in _exitfuncs:
		args,kwargs = _exitfuncs[func]
		func(*args,**kwargs)

atexit.register(_run_at_exit)

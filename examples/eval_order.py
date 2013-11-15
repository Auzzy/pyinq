from pyinq.tags import test
from pyinq.asserts import eval_equal,eval_raises

def unexpected():
	raise Exception("EXCEPTION")

def no_error():
	pass

@test
def unexpected_error_last():
	eval_equal(4, 5)
	eval_raises(IOError, unexpected)

@test
def unexpected_error_first():
	eval_raises(IOError, unexpected)
	eval_equal(4, 5)

@test
def fail_last():
	eval_equal(4, 5)
	eval_raises(IOError, no_error)

@test
def fail_first():
	eval_raises(IOError, no_error)
	eval_equal(4, 5)

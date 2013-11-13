from pyinq.results import (AssertResult,AssertEqualsResult,AssertInResult,
			  AssertRaisesResult,AssertInstanceResult,PyInqAssertError,
			  PyInqAssertEqualsError,PyInqAssertInError,
			  PyInqAssertInstanceError,PyInqAssertRaisesError,
			  PyInqFailError)
from pyinq.asserts import _asserts
from pyinq.asserts.ops import *

_equals_fact = _asserts.create_result(AssertEqualsResult,PyInqAssertEqualsError)
_in_fact = _asserts.create_result(AssertInResult,PyInqAssertInError)
_instance_fact = _asserts.create_result(AssertInstanceResult,PyInqAssertInstanceError)
_raises_fact = _asserts.create_result(AssertRaisesResult,PyInqAssertRaisesError)


# TODO
# This looks promising to replace my hcaky as hell assert factory, but still doesn't jive well with assert_raises. Look more into how to make this work, including rearranging assert_raises if necessary.
class AssertFactory(object):
	def __init__(self, compare, Result, Error, arg_count):
		self.compare = compare

		def factory(*args):
			def result(lineno, call, result):
				return Result(lineno, call, result, *args)
			def error(lineno, call):
				return Error(lineno, call, *args)
			if arg_count != len(args):
				raise TypeError("Function takes exactly {0} arguments ({1} given)".format(arg_count, len(args)))
			return result,error
		self.Factory = factory

	def assert_(*args):
		return _asserts.assert_base(compare(*args), self.Factory(*args))

	def assert_not(*args):
		return _asserts.assert_base(not compare(*args), self.Factory(*args))

	def eval(*args):
		return _asserts.eval_base(compare(*args), self.Factory(*args))

	def eval_not(*args):
		return _asserts.eval_base(not compare(*args), self.Factory(*args))

# eq = lambda actual,expected: actual == expected
# equal_fact = AssertFactory(eq, AssertEqualsResult, PyInqAssertEqualsResult, 2)
# def assert_equal
# 	return equal_fact.assert(actual, expected)
# def assert_not_equal
# 	return equal_fact.assert_not(actual, expected)
# def eval_equal
# 	return equal_fact.eval(actual, expected)
# def eval_not_equal
# 	return equal_fact.eval_not(actual, expected)

# test_func = lambda func:
# 
# raises_factory = AssertFactory(func, AssertRaisesResult, PyInqAssertRaisesError, 2)
# def assert_raises
# 	return raises_factory.assert()
# def eval_raises
# 	

##### ASSERTS #####

def assert_true(expr):
	return _asserts.assert_base(expr)
def assert_false(expr):
	return _asserts.assert_base(not expr)
def assert_none(expr):
	return _asserts.assert_base(expr is None)
def assert_not_none(expr):
	return _asserts.assert_base(expr is not None)
def assert_equal(actual, expected):
	return _asserts.assert_base(actual==expected,*_equals_fact(actual,expected))
def assert_not_equal(actual, expected):
	return _asserts.assert_base(actual!=expected)
def assert_is(actual, expected):
	return _asserts.assert_base(actual is expected,*_equals_fact(actual,expected))
def assert_is_not(actual, expected):
	return _asserts.assert_base(actual is not expected)
def assert_in(item, container):
	return _asserts.assert_base(item in container,*_in_fact(item,container))
def assert_not_in(item, container):
	return _asserts.assert_base(item not in container,*_in_fact(item,container))
def assert_is_instance(obj, cls):
	return _asserts.assert_base(isinstance(obj,cls),*_instance_fact(obj,cls))
def assert_is_not_instance(obj, cls):
	return _asserts.assert_base(not isinstance(obj,cls),*_instance_fact(obj,cls))
def assert_attrib(obj, name):
	return _asserts.assert_base(hasattr(obj,name))
def assert_not_attrib(obj, name):
	return _asserts.assert_base(not hasattr(obj,name))
def assert_raises(exception, func, *args, **kwargs):
	trace = test_raises(exception,func,*args,**kwargs)
	return _asserts.assert_base(bool(trace),*_raises_fact(trace,exception))


##### EVALS #####

def eval_true(expr):
	return _asserts.eval_base(expr)
def eval_false(expr):
	return _asserts.eval_base(not expr)
def eval_none(expr):
	return _asserts.eval_base(expr is None)
def eval_not_none(expr):
	return _asserts.eval_base(expr is not None)
def eval_equal(actual, expected):
	return _asserts.eval_base(actual==expected,_equals_fact(actual,expected)[0])
def eval_not_equal(actual, expected):
	return _asserts.eval_base(actual!=expected)
def eval_is(actual, expected):
	return _asserts.eval_base(actual is expected,_equals_fact(actual,expected)[0])
def eval_is_not(actual, expected):
	return _asserts.eval_base(actual is not expected)
def eval_in(item, container):
	return _asserts.eval_base(item in container,_in_fact(item,container)[0])
def eval_not_in(item, container):
	return _asserts.eval_base(item not in container,_in_fact(item,container)[0])
def eval_is_instance(obj, cls):
	return _asserts.eval_base(isinstance(obj,cls),_instance_fact(obj,cls)[0])
def eval_is_not_instance(obj, cls):
	return _asserts.eval_base(not isinstance(obj,cls),_instance_fact(obj,cls)[0])
def eval_attrib(obj, name):
	return _asserts.eval_base(hasattr(obj,name))
def eval_not_attrib(obj, name):
	return _asserts.eval_base(not hasattr(obj,name))
def eval_raises(exception, func, *args, **kwargs):
	trace = test_raises(exception,func,*args,**kwargs)
	return _asserts.eval_base(bool(trace),_raises_fact(trace,exception)[0])


##### FAIL #####

def fail(mess=""):
	lineno,_ = _asserts.get_call()
	raise PyInqFailError(lineno,mess)


##### ACCESS ######

def init_results(test_name):
	_asserts.init_results(test_name)

def clear_results():
	_asserts.clear_results()

def get_results():
	return _asserts.results

import operator

from pyinq.results import (AssertResult, AssertTruthResult, AssertEqualsResult,
			  AssertInResult, AssertInstanceResult, AssertAttribResult,
			  AssertRaisesResult, PyInqAssertError, PyInqAssertTruthError,
			  PyInqAssertEqualsError,PyInqAssertInError, PyInqAssertInstanceError,
			  PyInqAssertAttribError, PyInqAssertRaisesError, PyInqFailError)
from pyinq.asserts import _asserts
from pyinq.asserts import ops


truth_factory = _asserts.AssertFactory(operator.truth, AssertTruthResult, PyInqAssertTruthError, 1)
equal_factory = _asserts.AssertFactory(operator.eq, AssertEqualsResult, PyInqAssertEqualsError, 2)
is_factory = _asserts.AssertFactory(operator.is_, AssertEqualsResult, PyInqAssertEqualsError, 2)
in_factory = _asserts.AssertFactory(ops.in_, AssertInResult, PyInqAssertInError, 2) # operator.contains reverses the arguments, so it's useless to me
instance_factory = _asserts.AssertFactory(isinstance, AssertInstanceResult, PyInqAssertInstanceError, 2)
attrib_factory = _asserts.AssertFactory(hasattr, AssertAttribResult, PyInqAssertAttribError, 2)
raises_factory = _asserts.AssertFactory(ops.test_raises, AssertRaisesResult, PyInqAssertRaisesError, 4)


##### ASSERTS #####

def assert_true(expr):
	return truth_factory.assert_(expr)
def assert_false(expr):
	return truth_factory.assert_not(expr)
def assert_none(expr):
	return is_factory.assert_(expr, None)
def assert_not_none(expr):
	return is_factory.assert_not(expr, None)
def assert_equal(actual, expected):
	return equal_factory.assert_(actual, expected)
def assert_not_equal(actual, expected):
	return equal_factory.assert_not(actual, expected)
def assert_is(actual, expected):
	return is_factory.assert_(actual, expected)
def assert_is_not(actual, expected):
	return is_factory.assert_not(actual, expected)
def assert_in(item, container):
	return in_factory.assert_(item, container)
def assert_not_in(item, container):
	return in_factory.assert_not(item, container)
def assert_is_instance(obj, cls):
	return instance_factory.assert_(obj, cls)
def assert_is_not_instance(obj, cls):
	return instance_factory.assert_not(obj, cls)
def assert_attrib(obj, name):
	return attrib_factory.assert_(obj, name)
def assert_not_attrib(obj, name):
	return attrib_factory.assert_not(obj, name)
def assert_raises(exception, func, *args, **kwargs):
	return raises_factory.assert_(exception, func, args, kwargs)


##### EVALS #####

def eval_true(expr):
	return truth_factory.eval(expr)
def eval_false(expr):
	return truth_factory.eval_not(expr)
def eval_none(expr):
	return is_factory.eval(expr, None)
def eval_not_none(expr):
	return is_factory.eval_not(expr, None)
def eval_equal(actual, expected):
	return equal_factory.eval(actual, expected)
def eval_not_equal(actual, expected):
	return equal_factory.eval_not(actual, expected)
def eval_is(actual, expected):
	return is_factory.eval(actual, expected)
def eval_is_not(actual, expected):
	return is_factory.eval_not(actual, expected)
def eval_in(item, container):
	return in_factory.eval(item, container)
def eval_not_in(item, container):
	return in_factory.eval_not(item, container)
def eval_is_instance(obj, cls):
	return instance_factory.eval(obj, cls)
def eval_is_not_instance(obj, cls):
	return instance_factory.eval_not(obj, cls)
def eval_attrib(obj, name):
	return attrib_factory.eval(obj, name)
def eval_not_attrib(obj, name):
	return attrib_factory.eval_not(obj, name)
def eval_raises(exception, func, *args, **kwargs):
	return raises_factory.eval(exception, func, args, kwargs)


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

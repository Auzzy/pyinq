"""
Copyright (c) 2012, Austin Noto-Moniz (metalnut4@netscape.net)

Permission to use, copy, modify, and/or distribute this software for any purpose
with or without fee is hereby granted, provided that the above copyright notice
and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS
OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER
TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF
THIS SOFTWARE.
"""

from pyinq.results import (AssertEqualsResult,AssertInResult,AssertRaisesResult,
                          AssertInstanceResult,PyInqAssertEqualsError,
                          PyInqAssertInError,PyInqAssertInstanceError,
                          PyInqAssertRaisesError,PyInqFailError)
from pyinq.asserts import _asserts
from pyinq.asserts.ops import *

_equals_fact = _asserts.create_result(AssertEqualsResult,PyInqAssertEqualsError)
_in_fact = _asserts.create_result(AssertInResult,PyInqAssertInError)
_instance_fact = _asserts.create_result(AssertInstanceResult,PyInqAssertInstanceError)
_raises_fact = _asserts.create_result(AssertRaisesResult,PyInqAssertRaisesError)

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

"""
Copyright (c) 2012-2013, Austin Noto-Moniz (metalnut4@netscape.net)

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

from numbers import Number

from pyinq.asserts import *
from pyinq.results import *


##### ASSERTS #####

def run_assert_pass(func, *args):
    init_results("<TEST>")
    func(*args)
    results = get_results()
    try:
        assert len(results) == 1
    except AssertionError:
        raise AssertionError("Multiple results were recorded for this single assert call. Exactly 1 result should be generated.")
    
    return results[0]

def run_assert_fail(func, *args):
    init_results("<TEST>")
    try:
        func(*args)
        return None
    except PyInqError as err:
        return err

def check_assert_func(func, Pass, Fail, pass_args, fail_args):
    result = run_assert_pass(func,*pass_args)
    assert result
    assert type(result) is Pass
    
    result = run_assert_fail(func,*fail_args)
    assert result
    assert type(result) is Fail


def test_assert_true():
    pass_args = (True,)
    fail_args = (False,)
    check_assert_func(assert_true,AssertResult,PyInqAssertError,pass_args,fail_args)

def test_assert_false_pass():
    pass_args = (False,)
    fail_args = (True,)
    check_assert_func(assert_false,AssertResult,PyInqAssertError,pass_args,fail_args)

def test_assert_none():
    pass_args = (None,)
    fail_args = (1,)
    check_assert_func(assert_none,AssertResult,PyInqAssertError,pass_args,fail_args)

def test_assert_not_none():
    pass_args = ("Hello",)
    fail_args = (None,)
    check_assert_func(assert_not_none,AssertResult,PyInqAssertError,pass_args,fail_args)

def test_assert_equal():
    pass_args = (4,4)
    fail_args = (4,5)
    check_assert_func(assert_equal,AssertEqualsResult,PyInqAssertEqualsError,pass_args,fail_args)

def test_assert_not_equal():
    pass_args = (4,5)
    fail_args = (4,4)
    check_assert_func(assert_not_equal,AssertResult,PyInqAssertError,pass_args,fail_args)

def test_assert_is():
    pass_args = (int,int)
    fail_args = (int,Number)
    check_assert_func(assert_is,AssertEqualsResult,PyInqAssertEqualsError,pass_args,fail_args)

def test_assert_is_not():
    pass_args = (int,Number)
    fail_args = (int,int)
    check_assert_func(assert_is_not,AssertResult,PyInqAssertError,pass_args,fail_args)

def test_assert_is_instance():
    pass_args = (42,Number)
    fail_args = (42,str)
    check_assert_func(assert_is_instance,AssertInstanceResult,PyInqAssertInstanceError,pass_args,fail_args)

def test_assert_is_not_instance():
    pass_args = (42,str)
    fail_args = (42,Number)
    check_assert_func(assert_is_not_instance,AssertInstanceResult,PyInqAssertInstanceError,pass_args,fail_args)

def test_assert_in():
    pass_args = (5,[1,1,2,3,5,8,13,21])
    fail_args = (4,[1,1,2,3,5,8,13,21])
    check_assert_func(assert_in,AssertInResult,PyInqAssertInError,pass_args,fail_args)

def test_assert_not_in():
    pass_args = (4,[1,1,2,3,5,8,13,21])
    fail_args = (5,[1,1,2,3,5,8,13,21])
    check_assert_func(assert_not_in,AssertInResult,PyInqAssertInError,pass_args,fail_args)

def test_assert_attrib_pass():
    pass_args = (str(),"split")
    fail_args = (str(),"foo")
    check_assert_func(assert_attrib,AssertResult,PyInqAssertError,pass_args,fail_args)    

def test_assert_not_attrib():
    pass_args = (str(),"foo")
    fail_args = (str(),"split")
    check_assert_func(assert_not_attrib,AssertResult,PyInqAssertError,pass_args,fail_args)    

def test_assert_raises():
    pass_args = (ValueError,int,"hello")
    fail_args = (ValueError,int,"12345")
    check_assert_func(assert_raises,AssertRaisesResult,PyInqAssertRaisesError,pass_args,fail_args)


##### EVALS #####

def run_eval(func, *args):
    init_results("<TEST>")
    func(*args)
    results = get_results()
    try:
        assert len(results) == 1
    except AssertionError:
        raise AssertionError("Multiple results were recorded for this single eval call. Exactly 1 result should be generated.")
    
    return results[0]

def check_eval_func(func, Result, pass_args, fail_args):
    pass_result = run_eval(func,*pass_args)
    fail_result = run_eval(func,*fail_args)
    assert pass_result
    assert fail_result
    assert type(pass_result) is Result
    assert type(fail_result) is Result


def test_eval_true():
    pass_args = (True,)
    fail_args = (False,)
    check_eval_func(eval_true,AssertResult,pass_args,fail_args)

def test_eval_false_pass():
    pass_args = (False,)
    fail_args = (True,)
    check_eval_func(eval_false,AssertResult,pass_args,fail_args)

def test_eval_none():
    pass_args = (None,)
    fail_args = (1,)
    check_eval_func(eval_none,AssertResult,pass_args,fail_args)

def test_eval_not_none():
    pass_args = ("Hello",)
    fail_args = (None,)
    check_eval_func(eval_not_none,AssertResult,pass_args,fail_args)

def test_eval_equal():
    pass_args = (4,4)
    fail_args = (4,5)
    check_eval_func(eval_equal,AssertEqualsResult,pass_args,fail_args)

def test_eval_not_equal():
    pass_args = (4,5)
    fail_args = (4,4)
    check_eval_func(eval_not_equal,AssertResult,pass_args,fail_args)

def test_eval_is():
    pass_args = (int,int)
    fail_args = (int,Number)
    check_eval_func(eval_is,AssertEqualsResult,pass_args,fail_args)

def test_eval_is_not():
    pass_args = (int,Number)
    fail_args = (int,int)
    check_eval_func(eval_is_not,AssertResult,pass_args,fail_args)

def test_eval_is_instance():
    pass_args = (42,Number)
    fail_args = (42,str)
    check_eval_func(eval_is_instance,AssertInstanceResult,pass_args,fail_args)

def test_eval_is_not_instance():
    pass_args = (42,str)
    fail_args = (42,Number)
    check_eval_func(eval_is_not_instance,AssertInstanceResult,pass_args,fail_args)

def test_eval_in():
    pass_args = (5,[1,1,2,3,5,8,13,21])
    fail_args = (4,[1,1,2,3,5,8,13,21])
    check_eval_func(eval_in,AssertInResult,pass_args,fail_args)

def test_eval_not_in():
    pass_args = (4,[1,1,2,3,5,8,13,21])
    fail_args = (5,[1,1,2,3,5,8,13,21])
    check_eval_func(eval_not_in,AssertInResult,pass_args,fail_args)

def test_eval_attrib_pass():
    pass_args = (str(),"split")
    fail_args = (str(),"foo")
    check_eval_func(eval_attrib,AssertResult,pass_args,fail_args)    

def test_eval_not_attrib():
    pass_args = (str(),"foo")
    fail_args = (str(),"split")
    check_eval_func(eval_not_attrib,AssertResult,pass_args,fail_args)    

def test_eval_raises():
    pass_args = (ValueError,int,"hello")
    fail_args = (ValueError,int,"12345")
    check_eval_func(eval_raises,AssertRaisesResult,pass_args,fail_args)


##### FAIL #####
def test_fail():
    try:
        fail("This should fail.")
        raise AssertionError("The fail function did not cause a failure.")
    except PyInqFailError:
        pass

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

from pyinq.results import *


##### TEST ASSERT RESULTS #####

LINENO = 12
CALL = "assert_true(True)"
FAIL = "FAIL"
TRACE = "TRACE"
EXPECTED = IOError

def test_Result_true():
    check_Result(True)
    
def test_Result_false():
    check_Result(False)

def test_AssertResult_true():
    check_AssertResult(True)

def test_AssertResult_false():
    check_AssertResult(False)

def test_AssertEqualsResult_true():
    check_AssertEqualsResult(True,4,4)

def test_AssertEqualsResult_false():
    check_AssertEqualsResult(False,4,5)

def test_AssertInResult_true():
    check_AssertInResult(True,4,[1,2,4,8,16,32,64])

def test_AssertInResult_false():
    check_AssertInResult(False,4,[1,1,2,3,5,8,13])

def test_AssertInstanceResult_true():
    check_AssertInstanceResult(True,IOError,Exception)

def test_AssertInstanceResult_false():
    check_AssertInstanceResult(False,IOError,WindowsError)

def test_AssertRaisesResult_true():
    check_AssertRaisesResult(True,TRACE)

def test_AssertRaisesResult_false():
    check_AssertRaisesResult(False,"")

def test_ExpectedErrorResult_true():
    check_ExpectedErrorResult(True,LINENO)

def test_ExpectedErrorResult_false():
    check_ExpectedErrorResult(False,None)

def test_FailResult():
    result = FailResult(LINENO,FAIL)
    assert result.lineno == LINENO
    assert result.mess == FAIL
    assert result.result == False

def test_AssertError():
    result = AssertError(TRACE)
    assert result.trace == TRACE
    assert result.result is None


##### TEST RESULTS #####

NAME = "FOO"

def test_TestResult():
    test_result = TestResult(NAME)

    assert test_result.name == NAME
    assert not test_result.before
    assert not test_result.after

def test_TestResult_true():
    test_result = TestResult(NAME)
    test_result.extend(make_AssertResult_list(True,True,True))
    assert test_result.get_status() == True

def test_TestResult_false():
    test_result = TestResult(NAME)
    test_result.extend(make_AssertResult_list(True,True,False))
    assert test_result.get_status() == False

def test_TestClassResult():
    cls_result = TestClassResult(NAME)

    assert cls_result.name == NAME
    assert not cls_result.before
    assert not cls_result.after

def test_TestClassResult_true():
    cls_result = TestClassResult(NAME)
    cls_result.extend(make_TestResult_list(True,True,True))
    assert cls_result.get_status() == True

def test_TestClassResult_false():
    cls_result = TestClassResult(NAME)
    cls_result.extend(make_TestResult_list(True,True,False))
    assert cls_result.get_status() == False

def test_TestModuleResult():
    mod_result = TestModuleResult(NAME)

    assert mod_result.name == NAME
    assert not mod_result.before
    assert not mod_result.after

def test_TestModuleResult_true():
    mod_result = TestModuleResult(NAME)
    mod_result.extend(make_TestClassResult_list(True,True,True))
    assert mod_result.get_status() == True

def test_TestModuleResult_false():
    mod_result = TestModuleResult(NAME)
    mod_result.extend(make_TestClassResult_list(True,True,False))
    assert mod_result.get_status() == False

def test_TestSuiteResult():
    suite_result = TestSuiteResult(NAME)

    assert suite_result.name == NAME
    assert not suite_result.before
    assert not suite_result.after

def test_TestSuiteResult_true():
    suite_result = TestSuiteResult(NAME)
    suite_result.extend(make_TestModuleResult_list(True,True,True))
    assert suite_result.get_status() == True

def test_TestSuiteResult_false():
    suite_result = TestModuleResult(NAME)
    suite_result.extend(make_TestModuleResult_list(True,True,False))
    assert suite_result.get_status() == False



##### TEST ERRORS #####

def construct_call_str(name, args):
    arg_str = ",".join([str(arg) for arg in args])
    return "{name}({arg_str})".format(name=name,arg_str=arg_str)

def check_PyInqError(func_name, arg_dict, error_cls, result_cls, check_func):
    call = construct_call_str(func_name,arg_dict.values())
    error = error_cls(LINENO,call,**arg_dict)
    result = error.result()

    assert error.lineno == LINENO
    assert error.call == call
    for arg_name in arg_dict:
        assert getattr(error,arg_name) == arg_dict[arg_name]

    assert type(result) is result_cls
    check_func(state=False,lineno=LINENO,call=call,result=result,**arg_dict)


def test_PyInqAssertError():
    arg_dict = {}
    check_PyInqError("assert_true",arg_dict,PyInqAssertError,AssertResult,check_AssertResult)

def test_PyInqAssertEqualsError():
    arg_dict = {"actual":4, "expected":42}
    check_PyInqError("assert_equal",arg_dict,PyInqAssertEqualsError,AssertEqualsResult,check_AssertEqualsResult)

def test_PyInqAssertInError():
    arg_dict = {"item":4, "collection":[1,1,2,3,5,8,13,21]}
    check_PyInqError("assert_in",arg_dict,PyInqAssertInError,AssertInResult,check_AssertInResult)

def test_PyInqAssertInstanceError():
    arg_dict = {"obj":IOError, "cls":IndexError}
    check_PyInqError("assert_is_instance",arg_dict,PyInqAssertInstanceError,AssertInstanceResult,check_AssertInstanceResult)

def test_PyInqAssertRaisesError():
    arg_dict = {"expected":IOError, "trace":""}
    check_PyInqError("assert_raises",arg_dict,PyInqAssertRaisesError,AssertRaisesResult,check_AssertRaisesResult)

def test_PyInqFailError():
    arg_dict = {"mess":"This is a failure message."}
    error = PyInqFailError(LINENO,**arg_dict)
    result = error.result()

    assert error.lineno == LINENO
    assert error.mess == arg_dict["mess"]

    assert type(result) is FailResult
    assert result.lineno == LINENO
    assert result.mess == arg_dict["mess"]
    assert result.result == False


##### TEST HELPERS #####

def check_Result(state, result=None):
    if not result:
        result = Result(state)
    assert result.result == state

def check_AssertResult(state, lineno=LINENO, call=CALL, result=None):
    if not result:
        result = AssertResult(lineno,call,state)
    assert result.lineno == lineno
    assert result.call == call
    assert result.result == state

def check_AssertEqualsResult(state, actual, expected, lineno=LINENO, call=CALL, result=None):
    if not result:
        result = AssertEqualsResult(lineno,call,state,actual,expected)
    assert result.lineno == lineno
    assert result.call == call
    assert result.result == state
    assert result.actual == actual
    assert result.expected == expected

def check_AssertInResult(state, item, collection, lineno=LINENO, call=CALL, result=None):
    if not result:
        result = AssertInResult(lineno,call,state,item,collection)
    assert result.lineno == lineno
    assert result.call == call
    assert result.result == state
    assert result.item == item
    assert result.collection == collection

def check_AssertInstanceResult(state, obj, cls, lineno=LINENO, call=CALL, result=None):
    if not result:
        result = AssertInstanceResult(lineno,call,state,obj,cls)
    assert result.lineno == lineno
    assert result.call == call
    assert result.result == state
    assert result.obj_name == obj.__class__.__name__
    assert result.class_name == cls.__name__

def check_AssertRaisesResult(state, trace, lineno=LINENO, call=CALL, expected=EXPECTED, result=None):
    if not result:
        result = AssertRaisesResult(lineno,call,state,trace,expected)
    assert result.lineno == lineno
    assert result.call == call
    assert result.result == state
    assert remove_whitespace(result.trace) == remove_whitespace(trace)
    assert result.expected == expected.__name__

def check_ExpectedErrorResult(state, lineno, expected=EXPECTED, result=None):
    if not result:
        result = ExpectedErrorResult(state,expected,lineno)
    assert result.expected == expected.__name__
    assert result.lineno == lineno
    assert result.call is None
    assert result.result == state

def make_AssertResult_list(*state_list):
    return [AssertResult(LINENO,CALL,state) for state in state_list]

def make_TestResult_list(*state_list):
    result_list = []
    for state in state_list:
        result = TestResult(NAME)
        result.extend(make_AssertResult_list(state))
        result_list.append(result)
    return result_list

def make_TestClassResult_list(*state_list):
    result_list = []
    for state in state_list:
        result = TestClassResult(NAME)
        result.extend(make_TestResult_list(state))
        result_list.append(result)
    return result_list

def make_TestModuleResult_list(*state_list):
    result_list = []
    for state in state_list:
        result = TestModuleResult(NAME)
        result.extend(make_TestClassResult_list(state))
        result_list.append(result)
    return result_list



##### UTIL #####

def remove_whitespace(string):
    return ''.join([line.strip() for line in string.splitlines()])

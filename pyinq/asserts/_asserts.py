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

from pyinq.results import AssertResult,PyInqAssertError,TestResult
from pyinq.util import get_call_frame,get_func_args

results = None

def clear_results():
    global results
    results = None

def init_results(test_name):
    global results
    results = TestResult(test_name)

def get_call():
    call_frame = get_call_frame()
    return call_frame[2],call_frame[4][0].strip()

def assert_base(test, Result=AssertResult, Error=PyInqAssertError):
    lineno,call = get_call()
    result = Result(lineno,call,test)
    if result.result:
        results.append(result)
    else:
        raise Error(lineno,call)

def eval_base(test, Result=AssertResult):
    lineno,call = get_call()
    result = Result(lineno,call,test)
    results.append(result)

def create_result(Result=AssertResult, Error=PyInqAssertError):
    result_args = len(get_func_args(Result.__init__))
    assert_result_args = len(get_func_args(AssertResult.__init__))
    arg_len = result_args - assert_result_args
    
    def result_pair(*args):
        def result(lineno, call, expr_out):
            return Result(lineno,call,expr_out,*args)
        def error(lineno, call):
            return Error(lineno,call,*args)
        if len(args)!=arg_len:
            raise TypeError("function takes exactly {0} arguments ({1} given)".format(arg_len,len(args)))
        return result,error
    return result_pair

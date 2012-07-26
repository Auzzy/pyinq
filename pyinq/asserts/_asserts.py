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
    arg_len = len(get_func_args(Result.__init__)) - len(get_func_args(AssertResult.__init__))
    
    def result_pair(*args):
        def result(lineno, call, expr_out):
            return Result(lineno,call,expr_out,*args)
        def error(lineno, call):
            return Error(lineno,call,*args)
        if len(args)!=arg_len:
            raise TypeError("function takes exactly {0} arguments ({1} given)".format(arg_len,len(args)))
        return result,error
    return result_pair

from sys import exc_info

from pyinq.util import create_tb_str,get_trace_start
from pyinq.results import (TestResult,ExpectedErrorResult,PyInqAssertError,
                          PyInqFailError,UnexpectedError)
from pyinq import asserts

def handle_error(expected):
	exc_type,exc_value,trace_obj = exc_info()[:3]
	trace = get_trace_start(trace_obj)
	if expected and isinstance(exc_value,expected):
		lineno = trace[0][1]
		result = ExpectedErrorResult(True,expected,lineno)
		halt = False
	else:
		tb_str = create_tb_str(exc_type,exc_value,trace)
		result = UnexpectedError(tb_str)
		halt = True
	return result,halt

def handle_assert(test):
	try:
		test()
	except AssertionError:
		trace = get_trace_start(exc_info()[2])[0]
		lineno = trace[1]
		call = trace[3]
		raise PyInqAssertError(lineno,call)

def _test_runner(test):
	if test:
		halt = False
		expected = hasattr(test,"expected") and test.expected
		test_results = TestResult(test.name)
		asserts.init_results(test.name)
		
		try:
			handle_assert(test)
		except (PyInqAssertError,PyInqFailError) as mess:
			result = mess.result()
			test_results.append(result)
			halt = True
		except Exception:
			result,halt = handle_error(expected)
			test_results.append(result)
		else:
			if expected:
				result = ExpectedErrorResult(False,expected)
				test_results.append(result)
				halt = True
		finally:
			test_results[:0] = asserts.get_results()
			asserts.clear_results()
		
		return test_results,halt
	else:
		return None,False

def run_fixture(test):
	return _test_runner(test)

def run_test(test):
	return _test_runner(test)[0]

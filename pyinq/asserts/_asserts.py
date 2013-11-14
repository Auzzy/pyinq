from pyinq.results import AssertResult,PyInqAssertError,TestResult
from pyinq.util import get_call_frame,get_func_args

results = None

class AssertFactory(object):
	def __init__(self, compare_func, Result, Error, arg_count):
		self.compare_func = compare_func

		def factory(*args):
			def result(lineno, call, result):
				return Result(lineno, call, result, *args)
			def error(lineno, call):
				return Error(lineno, call, *args)
			if arg_count != len(args):
				raise TypeError("Function takes exactly {0} arguments ({1} given)".format(arg_count, len(args)))
			return result,error
		self.Factory = factory

	def assert_(self, *args):
		return self._assert_func(self.compare_func(*args), *self.Factory(*args))

	def assert_not(self, *args):
		return self._assert_func(not self.compare_func(*args), *self.Factory(*args))

	def eval(self, *args):
		return self._eval_func(self.compare_func(*args), self.Factory(*args)[0])

	def eval_not(self, *args):
		return self._eval_func(not self.compare_func(*args), self.Factory(*args)[0])

	def _assert_func(self, test, Result, Error):
		global results
		lineno,call = get_call()
		result = Result(lineno, call, test)
		if result.result:
			results.append(result)
		else:
			raise Error(lineno, call)

	def _eval_func(self, test, Result):
		global results
		lineno,call = get_call()
		result = Result(lineno, call, test)
		results.append(result)

def clear_results():
	global results
	results = None

def init_results(test_name):
	global results
	results = TestResult(test_name)

def get_call():
	call_frame = get_call_frame()
	return call_frame[2],call_frame[4][0].strip()

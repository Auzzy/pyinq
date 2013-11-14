class TestResultStruct(list):
	def __init__(self, name):
		super(TestResultStruct, self).__init__()
		self.name = name
		self.before = None
		self.after = None
	
class TestResultContainer(TestResultStruct):
	def get_status(self):
		passing = True
		for result in self:
			status = result.get_status()
			if status is None:
				return None
			elif passing and not status:
				passing = False
		return passing
	
	def append(self, value):
		if not isinstance(value, TestResultStruct):
			raise ValueError("Cannot directly append an assert result object. Please use one of the test result objects.")
		super(self, TestResultContainer).append(value)

class TestResult(TestResultStruct):
	def get_status(self):
		passing = True
		for test in self:
			if test.result is None:
				return None
			elif passing and not test.result:
				passing = False
		return passing

	def append(self, value):
		if isinstance(value, TestResultStruct):
			raise ValueError("Cannot append another test result object. TestResult may only contain assert result objects.")
		super(self, TestResult).append(value)

class TestClassResult(TestResultContainer):
	def append(self, value):
		if not isinstance(value, TestResult):
			raise ValueError("Expected the value to be a TestResult object. Type: {0}".format(type(value)))
		super(self, TestClassResult).append(value)

class TestModuleResult(TestResultContainer):
	def append(self, value):
		if not isinstance(value, TestResultStruct):
			raise ValueError("Expected the value to be a TestResult object. Type: {0}".format(type(value)))
		super(self, TestModuleResult).append(value)

class TestSuiteResult(TestResultContaineir):
	def append(self, value):
		if not isinstance(value, TestResultStruct):
			raise ValueError("Expected the value to be a TestResult object. Type: {0}".format(type(value)))
		super(self, TestSuiteResult).append(value)


##### ERRORS #####

class PyInqError(Exception):
	pass

class PyInqAssertError(PyInqError):
	def __init__(self, lineno, call):
		super(PyInqAssertError,self).__init__()
		self.lineno = lineno
		self.call = call
	
	def result(self):
		return AssertResult(self.lineno,self.call,False)

class PyInqAssertTruthError(PyInqAssertError):
	def __init__(self, lineno, call, value):
		super(PyInqAssertTruthError, self).__init__(lineno, call)
		self.value = value
	
	def result(self):
		return AssertTruthResult(self.lineno, self.call, False, self.value)

class PyInqAssertEqualsError(PyInqAssertError):
	def __init__(self, lineno, call, actual, expected):
		super(PyInqAssertEqualsError,self).__init__(lineno,call)
		self.actual = actual
		self.expected = expected
	
	def result(self):
		return AssertEqualsResult(self.lineno,self.call,False,self.actual,self.expected)

class PyInqAssertInError(PyInqAssertError):
	def __init__(self, lineno, call, item, collection):
		super(PyInqAssertInError,self).__init__(lineno,call)
		self.item = item
		self.collection = collection

	def result(self):
		return AssertInResult(self.lineno,self.call,False,self.item,self.collection)

class PyInqAssertInstanceError(PyInqAssertError):
	def __init__(self, lineno, call, obj, cls):
		super(PyInqAssertInstanceError,self).__init__(lineno,call)
		self.obj = obj
		self.cls = cls

	def result(self):
		return AssertInstanceResult(self.lineno,self.call,False,self.obj,self.cls)

class PyInqAssertAttribError(PyInqAssertError):
	def __init__(self, lineno, call, obj, attrib_name):
		super(PyInqAssertAttribError, self).__init__(lineno, call)
		self.obj = obj
		self.attrib_name = attrib_name

	def result(self):
		return AssertAttribResult(self.lineno, self.call, False, self.obj, self.attrib_name)

class PyInqAssertRaisesError(PyInqAssertError):
	def __init__(self, lineno, call, trace, expected):
		super(PyInqAssertRaisesError,self).__init__(lineno,call)
		self.expected = expected
		self.trace = trace

	def result(self):
		return AssertRaisesResult(self.lineno,self.call,False,"",self.expected)

class PyInqFailError(PyInqError):
	def __init__(self, lineno, mess):
		super(PyInqFailError,self).__init__()
		self.lineno = lineno
		self.mess = mess

	def result(self):
		return FailResult(self.lineno,self.mess)

##### RESULTS #####

def create_result_str(result, lines=[], args=[]):
	format_str = result + "\n\t" + "\n\t".join(lines)
	return format_str.format(*args)

class Result(object):
	def __init__(self, result):
		self.result = result
	
	def __str__(self):
		return str(self.result)

class AssertResult(Result):
	def __init__(self, lineno, call, result):
		super(AssertResult,self).__init__(bool(result))
		self.lineno = lineno
		self.call = call
	
	def __str__(self):
		return "{0} (line {1}): {2}".format(self.call,self.lineno,self.result)

class AssertTruthResult(AssertResult):
	def __init__(self, lineno, call, result, value):
		super(AssertTruthResult, self).__init__(lineno, call, result)
		self.value = value
	
	def __str__(self):
		result_str = super(AssertTruthResult, self).__str__()
		return create_result_str(result_str,
					["truth value: {0}"],
					args=(bool(self.value),))

class AssertEqualsResult(AssertResult):
	def __init__(self, lineno, call, result, actual, expected):
		super(AssertEqualsResult,self).__init__(lineno,call,result)
		self.actual = actual
		self.expected = expected
	
	def __str__(self):
		result_str = super(AssertEqualsResult,self).__str__()
		return create_result_str(result_str,
					["expected: {0}","actual:   {1}"],
					args=(self.expected,self.actual))

class AssertInResult(AssertResult):
	def __init__(self, lineno, call, result, item, collection):
		super(AssertInResult,self).__init__(lineno,call,result)
		self.item = item
		self.collection = collection
	
	def __str__(self):
		result_str = super(AssertInResult,self).__str__()
		return create_result_str(result_str,
					["collection: {0}","element:    {1}"],
					args=(self.collection,self.item))

class AssertInstanceResult(AssertResult):
	def __init__(self, lineno, call, result, obj, cls):
		super(AssertInstanceResult,self).__init__(lineno,call,result)
		self.obj_name = obj.__class__.__name__
		self.class_name = cls.__name__
	
	def __str__(self):
		result_str = super(AssertInstanceResult,self).__str__()
		return create_result_str(result_str,
					["expected type: {0}","object class:  {1}"],
					args=(self.class_name,self.obj_name))

class AssertAttribResult(AssertResult):
	def __init__(self, lineno, call, result, obj, attrib_name):
		super(AssertAttribResult,self).__init__(lineno, call, result)
		self.obj_name = obj.__class__.__name__
		self.attrib_name = attrib_name

	def __str__(self):
		result_str = super(AssertAttribResult, self).__str__()
		return create_result_str(result_str,
					["attrib name: {0}", "object class:  {1}"],
					args=(self.attrib_name, self.obj_name))

class AssertRaisesResult(AssertResult):
	def __init__(self, lineno, call, result, expected, func, args, kwargs):
		super(AssertRaisesResult,self).__init__(lineno,call,result)
		self.expected = expected.__name__
		trace_lines = ["    {0}".format(line) for line in result.splitlines()]
		self.trace = '\n'.join(trace_lines)
		self.func_str = self._create_func_str(func.func_name, args, kwargs)
	
	def _create_func_str(self, func_name, args, kwargs):
		args_str_list = [str(val) for val in args]
		kwargs_str_list = ["{0}={1}".format(key, kwargs[key]) for key in kwargs]
		params_str = ", ".join(args_str_list + kwargs_str_list)
		return "{0}({1})".format(func_name, params_str)

	def __str__(self):
		result_str = super(AssertRaisesResult,self).__str__()
		func_str_output = "function call: {0}".format(self.func_str)
		if self.trace:
			return '\n'.join([result_str, func_str_output, self.trace])
		else:
			return create_result_str(result_str,
						[func_str_output, "{0} did not occur"],
						args=(self.expected,))

class ExpectedErrorResult(AssertResult):
	def __init__(self, result, expected, lineno=None):
		super(ExpectedErrorResult,self).__init__(lineno,None,result)
		self.expected = expected.__name__
	
	def __str__(self):
		if self.result:
			return create_result_str("Expected error {0}",
						["Occurred at line {1}"],
						args=(self.expected,self.lineno))
		else:
			return create_result_str("Expected error {0}",
						["Did not occur"],
						args=(self.expected,))

class FailResult(Result):
	def __init__(self, lineno, mess):
		super(FailResult,self).__init__(False)
		self.lineno = lineno
		self.mess = mess

	def __str__(self):
		return create_result_str("User induced fail at line {0}",
					[self.mess],
					args=(self.lineno,))

class UnexpectedError(Result):
	def __init__(self, trace):
		super(UnexpectedError,self).__init__(None)
		self.trace = trace
	
	def __str__(self):
		return self.trace

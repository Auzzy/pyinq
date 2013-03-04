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

class TestStructResult(list):
    def __init__(self, name):
        super(TestStructResult,self).__init__()
        self.name = name
        self.before = None
        self.after = None
    
class TestResult(TestStructResult):
    def get_status(self):
        for test in self:
            if test.result is None:
                return None
            elif not test.result:
                return False
        return True

class TestContainerResult(TestStructResult):
    def get_status(self):
        for result in self:
            status = result.get_status()
            if status is None:
                return None
            elif not status:
                return False
        return True

class TestClassResult(TestContainerResult):
    pass

class TestModuleResult(TestContainerResult):
    pass

class TestSuiteResult(TestContainerResult):
    pass


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

class PyInqAssertRaisesError(PyInqAssertError):
    def __init__(self, lineno, call, trace, expected):
        super(PyInqAssertRaisesError,self).__init__(lineno,call)
        self.expected = expected

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
    output = result
    for line in lines:
        output += "\n\t{0}".format(line)
    return output.format(*args)

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

class AssertRaisesResult(AssertResult):
    def __init__(self, lineno, call, result, trace, expected):
        super(AssertRaisesResult,self).__init__(lineno,call,result)
        self.expected = expected.__name__
        trace_lines = ["    {0}".format(line) for line in trace.splitlines()]
        self.trace = '\n'.join(trace_lines)
    
    def __str__(self):
        result_str = super(AssertRaisesResult,self).__str__()
        if self.trace:
            return "{0}\n{1}".format(result_str,self.trace)
        else:
            return create_result_str(result_str,
                        ["{0} did not occur"],
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

class AssertError(Result):
    def __init__(self, trace):
        super(AssertError,self).__init__(None)
        self.trace = trace
    
    def __str__(self):
        return self.trace

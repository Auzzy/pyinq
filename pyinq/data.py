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

import pyinq.runner as runner
from pyinq.results import (TestResult,TestClassResult,TestSuiteResult,
                          TestModuleResult)

##### TEST FIXTURE DATA ######

class Fixture(object):
    def __init__(self, func, suite=None):
        self._func = func
        self.name = self._func.__name__ if self._func else None
        self.suite = suite
        self.class_name = None
    
    @property
    def func(self):
        return self._func

    def __call__(self):
        if self._func:
            print "\nRUNNING {0}...".format(self)
            self._func()

    def __str__(self):
        class_name = (self.class_name + '.') if self.class_name else ''
        name = class_name + self.name
        return "{0} FIXTURE \"{1}\"".format(type(self).__name__,name)

class BeforeSuite(Fixture):
    pass

class BeforeModule(Fixture):
    pass

class BeforeClass(Fixture):
    pass

class Before(Fixture):
    def _set_self(self, self_):
        if self._func:
            # DEPRECATED
            self._func.__globals__["this"] = self_
            
            self._func.__globals__["self"] = self_

class After(Fixture):
    def _set_self(self, self_):
        if self._func:
            # DEPRECATED
            self._func.__globals__["this"] = self_
            
            self._func.__globals__["self"] = self_

class AfterClass(Fixture):
    pass

class AfterModule(Fixture):
    pass

class AfterSuite(Fixture):
    pass

class DoNothing(Fixture):
    def __init__(self):
        super(DoNothing,self).__init__(None)
    
    def _set_self(self, self_):
        pass
    
    def __nonzero__(self):
        return False

##### TEST STORAGE #####

class Test(object):
    def __init__(self, test, name, class_name, expected):
        self._test = test
        self.name = name
        self.class_name = class_name
        self.expected = expected
    
    @property
    def test(self):
        return self._test

    def _set_self(self):
        global_dict = self._test.__globals__
        if self.class_name in global_dict and global_dict[self.class_name]:
            self_ = global_dict[self.class_name]()

            # DEPRECATED
            self._test.__globals__["this"] = self_
            
            self._test.__globals__["self"] = self_
            return self_
        else:
            return None
    
    def __call__(self):
        print "\nRUNNING Test \"{0}\"...".format(self)
        self._test()
    
    def __str__(self):
        class_name = (self.class_name + '.') if self.class_name else ''
        return class_name + self.name

class TestData(object):
    def __init__(self, name, test, expected, suite):
        self.name = name
        self.suite = suite
        
        self._test = Test(test,name,None,expected)
        self.before = DoNothing()
        self.after = DoNothing()
    
    @property
    def test(self):
        return self._test.test

    def finish(self, before, after, class_name):
        self.before = before
        self.after = after
        self._test.class_name = class_name
    
    def _set_self(self):
        self_ = self._test._set_self()
        if self_:
            if self.before:
                self.before._set_self(self_)
            if self.after:
                self.after._set_self(self_)

    def __call__(self):
        self._set_self()

        before_result,halt = runner.run_fixture(self.before)
        results = TestResult(self._test.name) if halt else runner.run_test(self._test)
        results.before = before_result
        results.after,halt = runner.run_fixture(self.after)

        return results
    
    def __str__(self):
        return str(self._test)

class TestClassData(list):
    def __init__(self, name=None, suite=None, before=DoNothing(), before_test=DoNothing(), after_test=DoNothing(), after=DoNothing()):
        super(TestClassData,self).__init__()
        self.name = name
        self.suite = suite
        self.before = before
        self.before_test = before_test
        self.after_test = after_test
        self.after = after
    
    def copy(self, empty=True):
        copy = TestClassData()
        copy.name = self.name
        copy.suite = self.suite
        copy.before = self.before
        copy.before_test = self.before_test
        copy.after_test = self.after_test
        copy.after = self.after
        if not empty:
            copy.extend(self)
        return copy

    def finish(self):
        for test_data in self:
            test_data.finish(self.before_test,self.after_test,self.name)

    def __call__(self):
        results = TestClassResult(self.name)

        results.before,halt = runner.run_fixture(self.before)
        if not halt:
            results.extend([test() for test in self])
        results.after,halt = runner.run_fixture(self.after)
        
        return results
    
    def __str__(self):
        test_list_str = ', '.join(str(test) for test in self)
        return "<Tests: [{0}]>".format(test_list_str)

class TestModuleData(list):
    def __init__(self, name=None, before=DoNothing(), after=DoNothing()):
        super(TestModuleData,self).__init__()
        self.name = name
        self.before = before
        self.after = after
    
    def copy(self, empty=True):
        copy = TestModuleData()
        copy.name = self.name
        copy.before = self.before
        copy.after = self.after
        if not empty:
            copy.extend(self)
        return copy

    def __call__(self, suite_name=None):
        results = TestModuleResult(self.name)

        print "\n\nMODULE \"{name}\"...".format(name=self.name)
        results.before,halt = runner.run_fixture(self.before)
        if not halt:
            results.extend([test_class() for test_class in self])
        results.after,halt = runner.run_fixture(self.after)

        return results

    def __str__(self):
        class_list_str = ', '.join(str(cls) for cls in self)
        return "<Classes: [{0}]>".format(class_list_str)

class TestSuiteData(list):
    def __init__(self, name=None, before=DoNothing(), after=DoNothing()):
        super(TestSuiteData,self).__init__()
        self.name = name
        self.before = before
        self.after = after
    
    def __call__(self):
        results = TestSuiteResult(self.name)
        
        results.before,halt = runner.run_fixture(self.before)
        if not halt:
            results.extend([module() for module in self])
        results.after,halt = runner.run_fixture(self.after)
        
        return results
    
    def __str__(self):
        modules_str = ', '.join(str(module) for module in self)
        return "<Suite ({0}): <Modules: [{1}]>>".format(self.name,modules_str)

import pyinq.runner as runner
from pyinq.results import (TestResult,TestClassResult,TestSuiteResult,
                          TestModuleResult)

default_name = "__main__"

##### TEST FIXTURE DATA ######

class Fixture(object):
    def __init__(self, func):
        self._func = func
        self.name = self._func.__name__ if self._func else None

    def complete(self, cls_name, cls):
        if self._func:
            self._func.__globals__[cls_name] = cls
    
    def get_func(self):
        return self._func

    def __call__(self):
        if self._func:
            print "\nRUNNING {0}...".format(self)
            self._func()

    def __str__(self):
        return "{0} FIXTURE \"{1}\"".format(type(self).__name__,self.name)

class BeforeSuite(Fixture):
    pass

class BeforeModule(Fixture):
    pass

class BeforeClass(Fixture):
    pass

class Before(Fixture):
    def _set_this(self, this):
        if self._func:
            self._func.__globals__["this"] = this

class After(Fixture):
    def _set_this(self, this):
        if self._func:
            self._func.__globals__["this"] = this

class AfterClass(Fixture):
    pass

class AfterModule(Fixture):
    pass

class AfterSuite(Fixture):
    pass

class DoNothing(Fixture):
    def __init__(self):
        super(DoNothing,self).__init__(None)
    
    def __nonzero__(self):
        return False

##### TEST STORAGE #####

class Test(object):
    def __init__(self, test, name, class_name, expected):
        self.test = test
        self.name = name
        self.class_name = class_name
        self.expected = expected
    
    def _set_this(self):
        global_dict = self.test.__globals__
        if self.class_name in global_dict and global_dict[self.class_name]:
            this = global_dict[self.class_name]() 
            self.test.__globals__["this"] = this
            return this
        else:
            return None
    
    def __call__(self):
        print "\nRUNNING Test \"{0}\"...".format(self)
        self.test()
    
    def __str__(self):
        return "{0}.{1}".format(self.class_name,self.name)

class TestData(object):
    def __init__(self, name, test, expected, suite):
        self.name = name
        self.class_name = default_name
        self.suite = suite
        
        self.test = Test(test,name,self.class_name,expected)
        self.before = DoNothing()
        self.after = DoNothing()
    
    def get_test(self):
        return self.test.test

    def _complete_class_name(self, class_name):
        self.class_name = class_name
        self.test.class_name = class_name

    def _complete_fixtures(self, before, after):
        self.before = before
        self.after = after
    
    def _set_this(self):
        this = self.test._set_this()
        if this:
            if self.before:
                self.before._set_this(this)
            if self.after:
                self.after._set_this(this)

    def __call__(self):
        self._set_this()

        before_result,halt = runner.run_fixture(self.before)
        results = TestResult(self.name) if halt else runner.run_test(self.test)
        results.before = before_result
        results.after,halt = runner.run_fixture(self.after)

        return results
    
    def __str__(self):
        return "{0}.{1}".format(self.class_name,self.name)

class TestClassData(list):
    def __init__(self, class_data=None):
        super(TestClassData,self).__init__()
        if class_data:
            self.before = class_data.before
            self.before_test = class_data.before_test
            self.after_test = class_data.after_test
            self.after = class_data.after
            self.name = class_data.name
        else:
            self.before = DoNothing()
            self.before_test = DoNothing()
            self.after_test = DoNothing()
            self.after = DoNothing()
            self.name =  default_name
        
        self.test_names = []

    def append(self, test):
        super(TestClassData,self).append(test)
        self.test_names.append(test.name)
    
    def find(self, test):
        for test_data in self:
            if test_data.get_test()==test:
                return test_data
        return None
    
    def has_test(self, name):
        return name in self.test_names

    def reset_fixtures(self):
        self.before = DoNothing()
        self.before_test = DoNothing()
        self.after_test = DoNothing()
        self.after = DoNothing()

    def _complete(self, class_name):
        self.name = class_name
        
        for test_data in self:
            test_data._complete_class_name(class_name)
        
        self._complete_fixtures()
    
    def _complete_fixtures(self):
        for test_data in self:
            test_data._complete_fixtures(self.before_test,self.after_test)

    def __eq__(self, other):
        return type(self)==type(other) and self.name==other.name

    def __call__(self):
        results = TestClassResult(self.name)

        results.before,halt = runner.run_fixture(self.before)
        if not halt:
            results.extend([test() for test in self])
        results.after,halt = runner.run_fixture(self.after)
        
        return results

class TestModuleData(list):
    def __init__(self, mod_data=None):
        super(TestModuleData,self).__init__()
        if mod_data:
            self.before = mod_data.before
            self.after = mod_data.after
            self.name = mod_data.name
        else:
            self.before = DoNothing()
            self.after = DoNothing()
            self.name = None
    
    def find(self, cls):
        for cls_data in self:
            if cls_data.name==cls.__name__:
                return cls_data
        return None
    
    def update_class(self, class_data):
        if class_data in self:
            self[self.index(class_data)] = class_data
        else:
            self.append(class_data)
    
    def __call__(self, suite_name=None):
        results = TestModuleResult(self.name)

        results.before,halt = runner.run_fixture(self.before)
        if not halt:
            results.extend([test_class() for test_class in self])
        results.after,halt = runner.run_fixture(self.after)

        return results

class TestSuiteData(list):
    def __init__(self, name=None):
        super(TestSuiteData,self).__init__()
        self.before = DoNothing()
        self.after = DoNothing()
        self.name = name
    
    def find(self, mod):
        for mod_data in self:
            if mod_data.name==mod.name:
                return mod_data
        return None

    def __call__(self):
        results = TestSuiteResult(self.name)
        
        results.before,halt = runner.run_fixture(self.before)
        if not halt:
            results.extend([module() for module in self])
        results.after,halt = runner.run_fixture(self.after)
        
        return results


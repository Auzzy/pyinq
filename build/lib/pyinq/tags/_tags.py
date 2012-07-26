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

from types import ClassType,FunctionType,TypeType

from pyinq.tags._util import (BeforeSuite,BeforeModule,BeforeClass,Before,After,
                             AfterClass,AfterModule,AfterSuite,TestSuiteData,
                 TestModuleData,TestClassData,TestData,DoNothing)

test_class = TestClassData()
module = TestModuleData()
suites = {None: TestSuiteData(None)}
suites[None].append(module)

test_classes ={}
class_modules = {}
fixture_data = {}

##### TEST FIXTURE REGISTRATION #####
def BeforeSuite_register(func, suite):
    if type(func) is FunctionType:
        if suite not in suites:
            suites[suite] = TestSuiteData(suite)
        suites[suite].before = BeforeSuite(func)
        fixture_data[func] = suites[suite]
        return func

def BeforeModule_register(func):
    if type(func) is FunctionType:
        module.before = BeforeModule(func)
        fixture_data[func] = module
        return func

def BeforeClass_register(func):
    if type(func) is FunctionType:
        test_class.before = BeforeClass(func)
        fixture_data[func] = test_class
        return func

def Before_register(func):
    if type(func) is FunctionType:
        test_class.before_test = Before(func)
        fixture_data[func] = test_class
        return func

def After_register(func):
    if type(func) is FunctionType:
        test_class.after_test = After(func)
        fixture_data[func] = test_class
        return func

def AfterClass_register(func):
    if type(func) is FunctionType:
        test_class.after = AfterClass(func)
        fixture_data[func] = test_class
        return func

def AfterModule_register(func):
    if type(func) is FunctionType:
        module.after = AfterModule(func)
        fixture_data[func] = module
        return func

def AfterSuite_register(func, suite):
    if type(func) is FunctionType:
        if suite not in suites:
            suites[suite] = TestSuiteData(suite)
        suites[suite].after = AfterSuite(func)
        fixture_data[func] = suites[suite]
        return func

##### TEST REGISTRATION #####

def Test_register(test, expected, suite):
    if suite not in suites:
        suites[suite] = TestSuiteData(suite)
    if type(test) is FunctionType:
        test_data = TestData(test.func_name,test,expected,suite)
        test_class.append(test_data)
        test_classes[test] = test_class
        return test

def TestClass_register(cls, class_suite):
    if type(cls) is ClassType or type(cls) is TypeType:
        this = extract_class_tests(cls)
        this._complete(cls.__name__)
        discover_suite_methods(this,cls)
        
        this_module = get_this_module(class_suite)
        log_class(cls,this_module)

        this_module.update_class(this)
        if class_suite is not None:
            module.update_class(this)
        
        test_class.reset_fixtures()

        return cls

def Skip(test, cond=True):
    if cond:
        if type(test) is FunctionType:
            _skip_test(test)
        elif type(test) is ClassType or type(test) is TypeType:
            if test in class_modules:
                _skip_class(test)
            else:
                _skip_current_class(test)
    else:
        return test

def _skip_fixture(func):
    if func in fixture_data:
        data = fixture_data[func]
        if func==data.before.get_func():
            data.before = DoNothing()
        elif func==data.after.get_func():
            data.after = DoNothing()
        elif type(data) is TestClassData:
            if func==data.before_test.get_func():
                data.before_test = DoNothing()
            elif func==data.after_test.get_func():
                data.after_test = DoNothing()

def _skip_test(test):
    if test in test_classes:
        this_class = test_classes[test]
        test_data = this_class.find(test)
        if test_data:
            this_class.remove(test_data)
    else:
        _skip_fixture(test)

def _skip_class(cls):
    if cls in class_modules:
        for this_module in class_modules[cls]:
            cls_data = this_module.find(cls)
            if cls_data:
                this_module.remove(cls_data)

def _skip_current_class(cls):
    extract_class_tests(cls)
    test_class.reset_fixtures()


##### HELPERS #####

def get_this_module(suite):
    if suite not in suites:
        suites[suite] = TestSuiteData(suite)
    
    if module in suites[suite]:
        this_module = suites[suite].find(module)
    else:
        this_module = TestModuleData(module)
        suites[suite].append(this_module)
    return this_module

def log_class(cls, this_module):
    if cls not in class_modules:
        class_modules[cls] = []
    if this_module not in class_modules[cls]:
        class_modules[cls].append(this_module)

def discover_suite_methods(this, cls):
    new_classes = {}
    for test in this:
        if test.suite not in new_classes:
            new_classes[test.suite] = TestClassData(this)
            test_classes[test.get_test()] = new_classes[test.suite]
        new_classes[test.suite].append(test)

    for suite in new_classes:
        this_module = get_this_module(suite)
        log_class(cls,this_module)
        
        if new_classes[suite] not in this_module:
            this_module.append(new_classes[suite])
        
def extract_class_tests(cls):
    this = TestClassData(test_class)
    for test in reversed(test_class[:]):
        if hasattr(cls,test.name) and not this.has_test(test.name):
            test_classes[test.get_test()] = this
            this.append(test)
            test_class.remove(test)
    return this

def cleanup():
    if test_class:
        test_class._complete_fixtures()
        module.append(test_class)
        discover_suite_methods(test_class,None)


def get_module():
    return module

def get_suite(suite=None):
    return suites[suite] if suite in suites else suites[None]

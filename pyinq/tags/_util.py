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

from types import ClassType,FunctionType,MethodType,TypeType

from pyinq.data import (BeforeSuite,BeforeModule,BeforeClass,Before,After,
                       AfterClass,AfterModule,AfterSuite,TestSuiteData,
                       TestModuleData,TestClassData,TestData,DoNothing)

fixtures = {BeforeSuite:[],
        BeforeModule:[],
        BeforeClass:[],
        Before:[],
        After:[],
        AfterClass:[],
        AfterModule:[],
        AfterSuite:[]}
test_list = []
test_classes = []
test_modules = []
suites = {}

suite_name_list = set()

##### TEST FIXTURE REGISTRATION #####
def BeforeSuite_register(func, suite):
    return _register_fixture(func,BeforeSuite,suite)

def BeforeModule_register(func):
    return _register_fixture(func,BeforeModule)

def BeforeClass_register(func):
    return _register_fixture(func,BeforeClass)

def Before_register(func):
    return _register_fixture(func,Before)

def After_register(func):
    return _register_fixture(func,After)

def AfterClass_register(func):
    return _register_fixture(func,AfterClass)

def AfterModule_register(func):
    return _register_fixture(func,AfterModule)

def AfterSuite_register(func, suite):
    return _register_fixture(func,AfterSuite,suite)

def _register_fixture(func, Fixture, suite=None):
    if type(func) is FunctionType:
        fixtures[Fixture].append(Fixture(func,suite))
        return func


##### TEST REGISTRATION #####

def Test_register(test, expected, suite):
    suite_name_list.add(suite)
    
    if type(test) is FunctionType:
        test_list.append(TestData(test.func_name,test,expected,suite))
        return test

def TestClass_register(cls, class_suite):
    suite_name_list.add(class_suite)

    if type(cls) is ClassType or type(cls) is TypeType:
        tests = pop_class_tests(cls)
        before_cls,before,after,after_cls = pop_class_fixtures(cls)
        name = cls.__name__
        data = TestClassData(name,class_suite,before_cls,before,after,after_cls)
        data.extend(tests)
        data.finish()
        
        test_classes.append(data)

        return cls


##### SKIP TESTS #####

def Skip(test, cond=True):
    if cond:
        if type(test) is FunctionType:
            _skip_test(test)
        elif type(test) is MethodType:
            _skip_class_test(test)
        elif type(test) is ClassType or type(test) is TypeType:
            test_class = _find_class(test)
            if test_class:
                _skip_class(test_class)
            else:
                _skip_current_class(test)
    else:
        return test

def _skip_test(func):
    if not _remove_test(func):
        _remove_fixture(func)

def _skip_class_test(meth):
    test_class = _find_class(meth.im_class)
    if test_class:
        for test in reversed(test_class):
            if meth.im_func==test.test:
                test_class.remove(test)
                return True
    return False

def _skip_class(test_class):
    test_classes.remove(test_class)

def _skip_current_class(cls):
    pop_class_tests(cls)
    pop_class_fixtures(cls)


def _find_class(cls):
    for test_class in test_classes:
        if test_class.name==cls.__name__:
            return test_class
    return None

def _remove_test(func):
    for test in reversed(test_list[:]):
        if func==test.test:
            test_list.remove(test)
            return True
    return False

def _remove_fixture(func):
    for fix_type in fixtures:
        for fixture in reversed(fixtures[fix_type][:]):
            if func==fixture.func:
                fixtures[fix_type].remove(fixture)
                return True
    return False


##### HELPERS #####

def pop_class_tests(cls):
    tests = []
    test_names = []
    for test in reversed(test_list[:]):
        if hasattr(cls,test.name) and test.name not in test_names:
            tests.append(test)
            test_names.append(test.name)
            test_list.remove(test)
    return tests

def _pop_fixture(Fixture, cls):
    fixture_list = fixtures[Fixture]
    if fixture_list and (not cls or hasattr(cls,fixture_list[-1].name)):
        fixture = fixture_list.pop()
        if cls:
            fixture.class_name = cls.__name__
        return fixture
    else:
        return DoNothing()

def pop_class_fixtures(cls):
    before_cls = _pop_fixture(BeforeClass,cls)
    before = _pop_fixture(Before,cls)
    after = _pop_fixture(After,cls)
    after_cls = _pop_fixture(AfterClass,cls)
    
    return before_cls,before,after,after_cls

def pop_module_fixtures(name):
    before_module,after_module = DoNothing(),DoNothing()
    
    if fixtures[BeforeModule]: # and fixtures[BeforeModule][-1].__module__==name:
        before_module = fixtures[BeforeModule].pop()
    if fixtures[AfterModule]: # and fixtures[AfterModule][-1].__module__==name:
        after_module = fixtures[AfterModule].pop()
    
    return before_module,after_module

def get_suite_fixtures(name):
    before_suite,after_suite = DoNothing(),DoNothing()
    
    for fixture in reversed(fixtures[BeforeSuite]):
        if fixture.suite==name:
            before_suite = fixture
            break
    for fixture in reversed(fixtures[AfterSuite]):
        if fixture.suite==name:
            after_suite = fixture
            break
    
    return before_suite,after_suite

def finish_module(name=None):
    before_cls,before,after,after_cls = pop_class_fixtures(None)
    cls_data = TestClassData(None,None,before_cls,before,after,after_cls)
    if test_list:
        cls_data.extend(test_list)
    cls_data.finish()
    
    before_module,after_module = pop_module_fixtures(name)
    module_data = TestModuleData(name,before_module,after_module)
    if cls_data:
        module_data.append(cls_data)
    if test_classes:
        module_data.extend(test_classes)

    if module_data:
        test_modules.append(module_data)
    
    reset_module()

def reset_module():
    global test_list,test_classes

    test_list = []
    test_classes = []
    fixtures[BeforeModule] = []
    fixtures[BeforeClass] = []
    fixtures[Before] = []
    fixtures[After] = []
    fixtures[AfterClass] = []
    fixtures[AfterModule] = []

def _build_cls_data(cls, suite_name):
    cls_data = cls.copy()
    for test in cls:
        if test.suite==suite_name:
            cls_data.append(test)
    return cls_data

def _build_module_data(module, suite_name):
    module_data = module.copy()
    for cls in module:
        if cls.suite==suite_name:
            module_data.append(cls)
        else:
            cls_data = _build_cls_data(cls,suite_name)
            if cls_data:
                module_data.append(cls_data)
    return module_data

def _build_default_suite():
    default_suite = None
    if default_suite not in suites:
        before_suite,after_suite = get_suite_fixtures(default_suite)
        suite_data = TestSuiteData(default_suite,before_suite,after_suite)
        suite_data.extend(test_modules)
        suites[default_suite] = suite_data
        if default_suite in suite_name_list:
            suite_name_list.remove(default_suite)

def build_suite(suite_name):
    if not suites:
        finish_module()
    
    # This must be here to use None when an invalid suite name is entered
    _build_default_suite()
    
    if suite_name and suite_name in suite_name_list:
        before_suite,after_suite = get_suite_fixtures(suite_name)
        suite_data = TestSuiteData(suite_name,before_suite,after_suite)

        for module in test_modules:
            module_data = _build_module_data(module,suite_name)
            if module_data:
                suite_data.append(module_data)
        
        suites[suite_name] = suite_data

def get_suite(name=None):
    suite = suites[name] if name in suites else TestSuiteData(name)
    return suite
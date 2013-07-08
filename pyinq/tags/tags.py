from pyinq.tags import _tags

def get_suite(suite=None):
	_tags.build_suite(suite)
	return _tags.get_suite(suite)

def finish_module(name):
	_tags.finish_module(name)

##### FIXTURES #####

def beforeSuite(func=None, **kwargs):
	suite = kwargs["suite"] if "suite" in kwargs else None
	if func is None:
		return lambda func: _tags.BeforeSuite_register(func,suite)
	else:
		return _tags.BeforeSuite_register(func,suite)

def beforeModule(func):
	return _tags.BeforeModule_register(func)

def beforeClass(func):
	return _tags.BeforeClass_register(func)

def before(func):
	return _tags.Before_register(func)

def after(func):
	return _tags.After_register(func)

def afterClass(func):
	return _tags.AfterClass_register(func)

def afterModule(func):
	return _tags.AfterModule_register(func)

def afterSuite(func=None, **kwargs):
	suite = kwargs["suite"] if "suite" in kwargs else None
	if func is None:
		return lambda func: _tags.AfterSuite_register(func,suite)
	else:
		return _tags.AfterSuite_register(func,suite)

##### FIXTURE ALIASES #####
# These are deprecated, but will be maintained for now due to the initial
# release. They will be removed for version 1.0 at the latest.

BeforeSuite = beforeSuite
BeforeModule = beforeModule
BeforeClass = beforeClass
Before = before
After = after
AfterClass = afterClass
AfterModule = afterModule
AfterSuite = afterSuite

##### TESTS #####

def test(func=None, **kwargs):
	expected = kwargs["expect"] if "expect" in kwargs else None
	
	# DEPRECATED
	expected = kwargs["expected"] if not expected and "expected" in kwargs else expected
	
	suite = kwargs["suite"] if "suite" in kwargs else None

	if func is None:
		return lambda func: _tags.Test_register(func,expected,suite)
	else:
		return _tags.Test_register(func,expected,suite)


def testClass(cls=None, **kwargs):
	suite = kwargs["suite"] if "suite" in kwargs else None

	if cls is None:
		return lambda cls: _tags.TestClass_register(cls,suite)
	else:
		return _tags.TestClass_register(cls,suite)

##### TEST ALIASES #####
# These are deprecated, but will be maintained for now due to the initial
# release. They will be removed for version 1.0 at the latest.

Test = test
TestClass = testClass

##### SKIPS #####

def skip(func):
	return _tags.Skip(func)

def skipIf(cond):
	return lambda func: _tags.Skip(func,cond)

def skipUnless(cond):
	return lambda func: _tags.Skip(func,not cond)

##### SKIP ALIASES #####
# These are deprecated, but will be maintained for now due to the initial
# release. They will be removed for version 1.0 at the latest.

Skip = skip
SkipIf = skipIf
SkipUnless = skipUnless

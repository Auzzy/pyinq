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

from pyinq.tags import _tags

def get_suite(suite=None):
    _tags.cleanup()
    return _tags.get_suite(suite)

def get_module():
    _tags.cleanup()
    return _tags.get_module()

##### FIXTURES #####

def BeforeSuite(func=None, **kwargs):
    suite = kwargs["suite"] if "suite" in kwargs else None
    if func is None:
        return lambda func: _tags.BeforeSuite_register(func,suite)
    else:
        return _tags.BeforeSuite_register(func,suite)

def BeforeModule(func):
    return _tags.BeforeModule_register(func)

def BeforeClass(func):
    return _tags.BeforeClass_register(func)

def Before(func):
    return _tags.Before_register(func)

def After(func):
    return _tags.After_register(func)

def AfterClass(func):
    return _tags.AfterClass_register(func)

def AfterModule(func):
    return _tags.AfterModule_register(func)

def AfterSuite(func=None, **kwargs):
    suite = kwargs["suite"] if "suite" in kwargs else None
    if func is None:
        return lambda func: _tags.AfterSuite_register(func,suite)
    else:
        return _tags.AfterSuite_register(func,suite)

##### TESTS #####

def Test(test=None, **kwargs):
    expected = kwargs["expected"] if "expected" in kwargs else None
    suite = kwargs["suite"] if "suite" in kwargs else None

    if test is None:
        return lambda test: _tags.Test_register(test,expected,suite)
    else:
        return _tags.Test_register(test,expected,suite)


def TestClass(cls=None, **kwargs):
    suite = kwargs["suite"] if "suite" in kwargs else None

    if cls is None:
        return lambda cls: _tags.TestClass_register(cls,suite)
    else:
        return _tags.TestClass_register(cls,suite)

##### SKIPS #####

def Skip(test):
    return _tags.Skip(test)

def SkipIf(cond):
    return lambda test: _tags.Skip(test,cond)

def SkipUnless(cond):
    return lambda test: _tags.Skip(test,not cond)

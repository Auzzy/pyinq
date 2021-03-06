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

import os
import re
import sys

from os.path import dirname,relpath,splitext
from importlib import import_module

FUNC_PREFIX = "test_"
MODULE_PREFIX = "test_"

def _is_test_func(func_name):
    return func_name.startswith(FUNC_PREFIX)

def _run_tests(module):
    test_names = [func_name for func_name in dir(module) if _is_test_func(func_name)]
    for test_name in test_names:
        func = getattr(module,test_name)
        if func.__module__ == module.__name__:
            print "TEST: " + test_name
            func()

def _is_test_file(filename):
    return filename.startswith(MODULE_PREFIX) and filename.endswith(".py")

def _get_module_names(prefix, files):
    if prefix:
        prefix += '.'
    return {prefix + splitext(module)[0] for module in files if _is_test_file(module)}

def _get_package_modules(folder):
    dirname = folder[0]
    packages = [fold for fold in dirname.split(os.sep) if fold and fold!=os.curdir]
    prefix = '.'.join(packages)
    return _get_module_names(prefix,folder[2])

def _discover_test_files():
    modules = set()
    for folder in os.walk(os.curdir):
        names = _get_package_modules(folder)
        modules.update(names)
    return modules

def run_tests():
    cwd = os.getcwd()
    os.chdir(dirname(__file__))
    
    modules = _discover_test_files()
    abs_root_path = os.getcwd()
    sys.path = [abs_root_path] + sys.path
    for module in modules:
        print "\nMODULE: " + module
        mod = import_module(module,package=__package__)
        _run_tests(mod)
    
    os.chdir(cwd)

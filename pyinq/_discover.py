import os
import sys
import re
from os.path import join,normpath,splitext
from importlib import import_module

import _pyinq as _pyinq
from pyinq.tags import tags

MAIN = "__main__.py"
PACKAGE = "__init__.py"
MODULE = ".py"
	
def _import_modules(root, modules):
	abs_root_path = normpath(join(os.getcwd(),root))
	sys.path = [abs_root_path] + sys.path
	_pyinq._discovery_enabled = False
	for module in modules:
		import_module(module)
		tags.finish_module(module)
	_pyinq._discovery_enabled = True
	sys.path.remove(abs_root_path)

def _is_module(filename):
	return filename.endswith(MODULE)

def _is_special(filename):
	return filename.startswith(PACKAGE) or filename.startswith(MAIN)

def _is_test_module(mod, pattern):
	return _is_module(mod) and re.match(pattern,mod) and not _is_special(mod)

def _get_module_names(prefix, files, pattern):
	if prefix:
		prefix += '.'
	return {prefix + splitext(mod)[0] for mod in files if _is_test_module(mod,pattern)}

def _get_package_modules(folder, pattern):
	dirname = normpath(folder[0])
	packages = [fold for fold in dirname.split(os.sep) if fold and fold!=os.curdir]
	prefix = '.'.join(packages)
	return _get_module_names(prefix,folder[2],pattern)

def _is_package(folder_entry):
	return PACKAGE in folder_entry[2]

def _discover_modules(root, pattern):
	cwd = os.getcwd()
	os.chdir(root)
	
	fs_walk = os.walk(os.curdir)

	root_fold = next(fs_walk)
	modules = _get_package_modules(root_fold,pattern)
	for folder in fs_walk:
		if _is_package(folder):
			names = _get_package_modules(folder,pattern)
			modules.update(names)
		else:
			while folder[1]:
				del folder[1][0]
	
	os.chdir(cwd)

	_import_modules(root,sorted(modules))

def discover_tests(root=os.curdir, pattern=".*", suite_name=None):
	print root
	_discover_modules(root,pattern)
	return tags.get_suite(suite_name)

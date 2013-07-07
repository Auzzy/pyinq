import pyinq._atexit as atexit
from pyinq import printers,tags
from pyinq._discover import discover_tests as _discover_tests
from pyinq.tests import run_tests
from pyinq.parsers import install_main_parser,get_args

_discovery_enabled = True

def test_pyinq(**kwargs):
	atexit.unregister(_run_at_exit)
	run_tests()

def discover_tests_api(root, pattern=".*", suite_name=None):
	if _discovery_enabled:
		atexit.unregister(_run_at_exit)
		return _discover_tests(root,pattern,suite_name)

def discover_tests_cmd(root, pattern=".*", **args):
	if _discovery_enabled:
		atexit.unregister(_run_at_exit)
		_discover_tests(root,pattern,args["suite"])
		run_all(args)

def _run_at_exit():
	args,name = get_args()
	if args:
		run_all(args)

def run_all(args):
	kwargs = {"html":args["html"]}

	suite = tags.get_suite(args["suite"])
	
	if suite:
		report = suite()

		printer = printers.html if args["html"] else printers.cli
		printers.print_report(report,printer,**kwargs)

install_main_parser()
atexit.register(_run_at_exit)

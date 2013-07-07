import sys

from argparse import ArgumentParser

from pyinq.parsers import discovery,main,test

_parser = None
_argv = None
_args = None

class Parsers(object):
	TEST = test.NAME
	DISCOVERY = discovery.NAME

def _install_test_parser(command_parsers):
	test_parser = command_parsers.add_parser(test.NAME)
	test_parser = test.compose(test_parser)
	
	defaults = {"get_args":test.get_args, "parser":test.NAME}
	test_parser.set_defaults(**defaults)

def _install_discovery_parser(command_parsers):
	discovery_parser = command_parsers.add_parser(discovery.NAME)
	discovery_parser = discovery.compose(discovery_parser)
	
	defaults = {"get_args":discovery.get_args, "parser":discovery.NAME}
	discovery_parser.set_defaults(**defaults)

def install_command_parser(**kwargs):
	global _parser

	_parser = ArgumentParser(**kwargs)
	command_parsers_help = "Specify a command to the PyInq package."
	command_parsers = _parser.add_subparsers(help=command_parsers_help)
	_install_discovery_parser(command_parsers)
	_install_test_parser(command_parsers)

	_parser.usage = "python -m " + _parser.format_usage().split(':')[1].strip()

def install_main_parser(prog=None):
	global _parser
	_parser = main.compose(prog=prog)

	defaults = {"get_args":main.get_args, "parser":main.NAME}
	_parser.set_defaults(**defaults)

def get_args():
	global _args,_argv,_name
	if _argv==sys.argv:
		return (_args,_name) if _args else (None,None)
	else:
		_argv = sys.argv
		
		args = _parser.parse_args()
		_args = args.get_args(args)
		_name = args.parser if hasattr(args,"parser") else None
		return _args,_name

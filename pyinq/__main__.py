"""
This is included to allow for test discovery from the command line
"""
from pyinq.parsers import install_command_parser,get_args,Parsers
from pyinq._pyinq import discover_tests_cmd,test_pyinq

install_command_parser(prog=__package__)
args,name = get_args()
if name==Parsers.DISCOVERY:
	discover_tests_cmd(**args)
elif name==Parsers.TEST:
	test_pyinq(**args)

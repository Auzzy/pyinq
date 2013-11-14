from os.path import basename,splitext

from argparse import ArgumentParser,FileType

NAME = "__main__"
_prog = None

def compose(parser=None, **kwargs):
	global _prog

	if not parser:
		parser = ArgumentParser(**kwargs)
	parser.add_argument("--html",nargs='?',type=FileType('w'),default=False, metavar="FILE",
			help="Where to place the HTML test report (default: stdout)")
	parser.add_argument("--suite",default=None,
			help="The suite to run. If not provided, all tests are run.")
	
	_prog = parser.prog
	
	return parser

def get_args(args):
	html = args.html
	if html is None:
		test_filename = splitext(basename(_prog))[0] if _prog else "report.html"
		html_filename = "{0}_output.html".format(test_filename)
		html = open(html_filename,'w')
	
	return {"html":html, "suite":args.suite}

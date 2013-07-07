from argparse import ArgumentParser

NAME = "test"

def compose(parser=None, **kwargs):
	if not parser:
		parser = ArgumentParser(**kwargs)
	
	parser.usage = "python -m " + parser.format_usage().split(':')[1].strip()

	return parser

def get_args(args):
	return {}

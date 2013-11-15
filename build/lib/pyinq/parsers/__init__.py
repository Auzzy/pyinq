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

import sys

from argparse import ArgumentParser

from pyinq.parsers import discovery,main

_parser = None
_argv = None
_args = None

class Parsers(object):
    DISCOVERY = discovery.NAME

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

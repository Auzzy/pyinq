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
from os.path import exists,isdir
from argparse import ArgumentParser,ArgumentTypeError

from pyinq.parsers import main

NAME = "discover"

def _directory(arg):
    if exists(arg) and isdir(arg):
        return arg
    raise ArgumentTypeError("Provided path is not an existing directory.")

def _regex(arg):
    try:
        re.compile(arg)
        return arg
    except re.error:
        raise

def compose(parser=None, **kwargs):
    if not parser:
        parser = ArgumentParser(**kwargs)
    
    root_help_dict = {"curdir":os.curdir, "cwd":os.getcwd()}
    parser.add_argument("root",type=_directory,
            help=("The directory to begin test discovery. Use '{curdir}' " + \
            "for the current working directory: {cwd}").format(**root_help_dict))
    parser.add_argument("-p","--pattern",default=".*",type=_regex,
            help="Only modules whose name fits this pattern will be " + \
                 "searched. (default: %(default)s)")

    main.compose(parser)
    
    parser.usage = "python -m " + parser.format_usage().split(':')[1].strip()

    return parser

def get_args(args):
    main_args = main.get_args(args)
    discover_args = {"root":args.root, "pattern":args.pattern}
    discover_args.update(main_args)
    return discover_args

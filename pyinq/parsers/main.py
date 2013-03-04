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

from os.path import basename,splitext

from argparse import ArgumentParser,FileType

NAME = "__main__"
_prog = None

def compose(parser=None, **kwargs):
    global _prog

    if not parser:
        parser = ArgumentParser(**kwargs)
    parser.add_argument("--html",nargs='?',type=FileType('w'),default=False,
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

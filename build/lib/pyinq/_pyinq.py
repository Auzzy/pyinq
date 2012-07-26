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

import atexit
from argparse import ArgumentParser,FileType

from pyinq import printers,tags


parser = ArgumentParser()
parser.add_argument("--html",nargs='?',type=FileType('w'),default=False,
        help="Where to place the HTML test report " + \
        "(default: None (outputs to standard out))")
parser.add_argument("--suite",default=None,
        help="The suite to run. If not provided, all tests are run.")

def get_args():
    args = parser.parse_args()

    html = args.html
    if html is None:
        from os.path import basename,splitext
        test_filename = splitext(basename(parser.prog))[0]
        html_filename = "{0}_output.html".format(test_filename)
        html = open(html_filename,'w')

    suite = args.suite

    return suite,html

def run_all():
    suite_name,html = get_args()
    kwargs = {"html":html}

    suite = tags.get_suite(suite_name)
    report = suite()

    printer = printers.html if html else printers.cli
    printers.print_report(report,printer,**kwargs)

atexit.register(run_all)

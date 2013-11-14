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
        _discover_tests(root,pattern)
        return tags.get_suite(suite_name)

def discover_tests_cmd(root, pattern=".*", **args):
    if _discovery_enabled:
        atexit.unregister(_run_at_exit)
        _discover_tests(root,pattern)
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

        printer = printers.html if args["html"] else printers.get_default()
        printers.print_report(report,printer,**kwargs)

install_main_parser()
atexit.register(_run_at_exit)

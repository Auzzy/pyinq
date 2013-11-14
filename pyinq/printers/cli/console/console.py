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

from pyinq.printers.cli.console.color import (set_fore,set_back,BLUE,GREEN,RED,
                                             BLACK)
from pyinq.printers import AbstractPrinter

class Printer(AbstractPrinter):
    def title(self, title):
        print "\n\n{0}".format(title.upper())

    def section(self, label, name, nl=True):
        if name:
            section = "\n{label}: {name}".format(label=label.upper(),name=name)
            print section + ('\n' if nl else "")
        elif nl:
            print

    def log_test(self, label, results):
        print "{label}: {name}".format(label=label,name=results.name)

        if results:
            self._print_status(results)
            self._print_results(results)
        else:
            self._print_no_asserts()

        Printer._reset_colors()
        print

    def log_fixture(self, label, fixture):
        self.log_test(label,fixture)

    def cleanup(self):
        Printer._reset_colors()

    @staticmethod
    def _reset_colors():
        set_fore()
        set_back()

    @staticmethod
    def _print_result(result):
        if result.result is None:
            set_fore(BLUE,True)
        elif result.result:
            set_fore(GREEN,True)
        else:
            set_fore(RED,True)
        print result
        Printer._reset_colors()

    @staticmethod
    def _print_results(results):
        for result in results:
            Printer._print_result(result)

    @staticmethod
    def _print_status(results):
        status = results.get_status()
        if status is None:
            set_back(BLUE,True)
            print "ERROR",
        elif status:
            set_back(GREEN)
            print "PASSED",
        else:
            set_back(RED,True)
            print "FAILED",
        Printer._reset_colors()
        print

    @staticmethod
    def _print_no_asserts():
        set_fore(BLACK)
        set_back(BLACK,True)
        print "NO ASSERTS",
        Printer._reset_colors()
        print

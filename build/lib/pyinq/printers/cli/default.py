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

from pyinq.printers import AbstractPrinter

class Printer(AbstractPrinter):
    def title(self, title):
        print "\n\n{0}".format(title.upper())

    def section(self, label, name):
        print "\n{label}: {name}\n".format(label=label.upper(),name=name)

    def log_test(self, label, results):
        print "{label}: {name}".format(label=label,name=results.name)
        if results:
            Printer._print_status(results)
            Printer._print_results(results)
        else:
            Printer._print_no_asserts()
        print
        
    def log_fixture(self, label, fixture):
        self.log_test(label,fixture)

    @staticmethod
    def _print_results(results):
        for result in results:
            print result

    @staticmethod
    def _print_status(self, results):
        status = results.get_status()
        if status is None:
            print "ERROR"
        elif status:
            print "PASSED"
        else:
            print "FAILED"

    @staticmethod
    def _print_no_asserts(self):
        print "NO ASSERTS"

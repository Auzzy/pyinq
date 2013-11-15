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

from os.path import dirname,join as path_join
from pyinq.printers import AbstractPrinter


##### PRINTER INTERFACE #####

class Printer(AbstractPrinter):
    def __init__(self, **kwargs):
        super(Printer,self).__init__()
        if "html" not in kwargs:
            raise ValueError("The HTML Printer requires the \"html\" argument.")
        self.html = kwargs["html"]
        self._title = ""
        self._body = ""

    def title(self, name):
        self._title = name

    def section(self, label, name, nl=True):
        if name:
            self._body += "<p class=\"section\">{label}: {name}</p>".format(label=label,name=name)
        elif nl:
            self._body += "<br />"

    def log_test(self, label, results):
        args = {"label":label, "name":results.name}
        self._body += "<p class=\"testname\">{label}: {name}</p>".format(**args)

        if results:
            self._body += Printer._log_status(results.get_status())
            self._body += Printer._log_results(results)
        else:
            self._body += Printer._log_no_asserts()
        
        self._body += "<br />"
    
    def log_fixture(self, label, fixture):
        self.log_test(label,fixture)

    def cleanup(self):
        file_dir = dirname(__file__)
        css = open(path_join(file_dir,"css.css"),'r').read()
        
        report = ("<html>" + \
            "<head>" + \
            "<title>{title}</title>" + \
            "<style>{css}</style>" + \
            "</head>" + \
            "<body>" + \
            "<h1>{title}</h1>" + \
            "{body}" + \
            "</body>" + \
            "</html>").format(title=self._title,css=css,body=self._body)
        
        self.html.write(report)

        print "\nHTML report generated at {0}.".format(self.html.name)

    @staticmethod
    def _get_status_name(status):
        if status is None:
            return "error"
        elif status:
            return "passed"
        else:
            return "failed"

    @staticmethod
    def _format_result(result):
        status_name = Printer._get_status_name(result.result)
        args = {"status":status_name, "result":result}
        return "<span class=\"result {status}\">{result}</span>".format(**args)

    @staticmethod
    def _log_results(results):
        formatted_results = [Printer._format_result(result) for result in results]
        formatted_test = "<br />".join(formatted_results)
        return "<p class=\"test\">{0}</p>".format(formatted_test)

    @staticmethod
    def _log_status(status):
        status_name = Printer._get_status_name(status)
        args = {"class_name":status_name, "name":status_name.upper()}
        return "<p class=\"status {class_name}\">{name}</p>".format(**args)

    @staticmethod
    def _log_no_asserts():
        return "<p class=\"noasserts\">NO ASSERTS</p>"

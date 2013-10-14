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

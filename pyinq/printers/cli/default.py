from pyinq.printers import AbstractPrinter

class Printer(AbstractPrinter):
	def title(self, title):
		print "\n\n{0}".format(title.upper())

	def section(self, label, name, nl=True):
		if name:
			section = "\n{label}: {name}".format(label=label.upper(),name=name)
			print section + ('\n' if nl else '')
		elif nl:
			print

	def log_test(self, label, results):
		print "\n{label}: {name}".format(label=label,name=results.name)
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
	def _print_status(results):
		status = results.get_status()
		if status is None:
			print "ERROR"
		elif status:
			print "PASSED"
		else:
			print "FAILED"

	@staticmethod
	def _print_no_asserts():
		print "NO ASSERTS"

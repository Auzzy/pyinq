
class AbstractPrinter(object):
	"""
	An abstract class for creating Printers, used to output the results
	of the executed tests.
	"""
	
	mess = "The \"{func}\" method is not implemented for the type {type}"

	def __init__(self):
		if type(self) is AbstractPrinter:
			raise TypeError("Can't instantiate the abstract base class Printer")

	def title(self, name):
		"""Logs the report title."""
		name = self.__class__.__name__
		err = AbstractPrinter.mess.format(func="title",type=name)
		raise NotImplementedError(err)
	
	def section(self, label, name, nl=True):
		"""Logs a section header."""
		name = self.__class__.__name__
		err = AbstractPrinter.mess.format(func="section",type=name)
		raise NotImplementedError(err)

	def log_test(self, label, result):
		"""
		Logs the results of a single test (TestResult object),
		labeled with the provided label.
		"""
		name = self.__class__.__name__
		err = AbstractPrinter.mess.format(func="log_test",type=name)
		raise NotImplementedError(err)

	def log_fixture(self, label, result):
		"""
		Logs the results of a single test (TestResult object),
		labeled with the provided label.
		"""
		name = self.__class__.__name__
		err = AbstractPrinter.mess.format(func="log_fixture",type=name)
		raise NotImplementedError(err)

	def cleanup(self):
		"""Perform required cleanup operations, such as writing to a file."""
		pass

import pyinq.printers.cli
import pyinq.printers.html

def get_default():
	return pyinq.printers.cli

def print_report(suite, printer_mod=None, **kwargs):
	def log_fixture(label, fixture):
		if fixture:
			printer.log_fixture(label,fixture)
	
	printer_mod = printer_mod if printer_mod else get_default()
	printer = printer_mod.Printer(**kwargs)

	try:
		printer.title("Test Report")

		log_fixture("Before Suite",suite.before)
		for module in suite:
			printer.section("Module",module.name,nl=False)
			log_fixture("Before Module",module.before)

			for cls in sorted(module, key=lambda cls: cls.name):
				printer.section("Class",cls.name)
				log_fixture("Before Class",cls.before)

				for test in sorted(cls, key=lambda test: test.name):
					before_label = "Before \"{0}\"".format(test.name)
					log_fixture(before_label,test.before)
					
					if not test.before or test.before[-1].result:
						printer.log_test("Test",test)
					
					after_label = "After \"{0}\"".format(test.name)
					log_fixture(after_label,test.after)

				log_fixture("After Class",cls.after)

			log_fixture("After Module",module.after)

		log_fixture("After Suite",suite.after)

	finally:
		printer.cleanup()

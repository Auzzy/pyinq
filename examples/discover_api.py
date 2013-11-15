from pyinq import discover_tests
from pyinq import printers

suite = discover_tests('examples', suite_name="hello")
if suite:
	report = suite()
	printers.print_report(report)


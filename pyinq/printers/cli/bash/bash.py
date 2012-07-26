from pyinq.printers.cli.bash.color import color_print,WHITE,BLUE,GREEN,RED,BLACK
from pyinq.printers import AbstractPrinter

class Printer(AbstractPrinter):
    def title(self, title):
        color_print("\n\n{0}".format(title.upper()),fore=WHITE.bold())

    def section(self, label, name):
        line = "\n{label}: {name}\n".format(label=label.upper(),name=name)
        color_print(line,fore=WHITE.bold())

    def log_test(self, label, results):
        line = "{label}: {name}".format(label=label,name=results.name)
        color_print(line,fore=WHITE.bold())

        if results:
            Printer._print_status(results)
            Printer._print_results(results)
        else:
            Printer._print_no_asserts()

        print

    def log_fixture(self, label, fixture):
        self.log_test(label,fixture)

    @staticmethod
    def _print_result(result):
        if result.result is None:
            color_print(result,fore=BLUE.bold())
        elif result.result:
            color_print(result,fore=GREEN.bold())
        else:
            color_print(result,fore=RED.bold())

    @staticmethod
    def _print_results(results):
        for result in results:
            Printer._print_result(result)

    @staticmethod
    def _print_status(results):
        status = results.get_status()
        if status is None:
            color_print("ERROR",back=BLUE.bold())
        elif status:
            color_print("PASSED",back=GREEN.bold())
        else:
            color_print("FAILED",back=RED.bold())
    
    @staticmethod
    def _print_no_asserts():
        color_print("NO ASSERTS",fore=BLACK.bold(),back=WHITE)

import platform
import sys

system = platform.system()

if system=="Windows":
    from pyinq.printers.cli.console import Printer
elif system=="Linux" and sys.stdout.isatty:
    from pyinq.printers.cli.bash import Printer
else:
    from pyinq.printers.cli.default import Printer

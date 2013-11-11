:mod:`pyinq.printers`
=====================

PyInq includes a couple default printers, as well as some functions for interacting with them, and the ability to create your own.

Note that the printer infrastructure will be getting a bit of an overhaul in order to make it easier to use, cleaner, and more flexible. Thus, if the module cannot currently handle your needs, check back later. In the mean time, you can write a custom one using :ref:`discovery-api`.

.. function:: get_default()

Retrieves the module that PyInq uses as its default.
        
.. function:: print_report(result, printer=None, \*\*kwargs)

Prints a report on the given result object using the provided printer and arguments.

``result`` must be a :class:`TestSuiteResult` object. The behavior if it's not is undefined. This requirement will be changed to any result object in upcoming versions.

``printer`` must be a module or package that can load a class named ``Printer``. The ``Printer`` class defines the actual output formats by subclassing :class:`AbstractPrinter`, while this function defines the order of output. Again, this limitation will be relaxed in upcoming versions.

``kwargs`` allows arguments specifi to the given printer to be passed through.


AbstractPrinter
---------------
The :class:`AbstractPrinter` forms the base of any printer. It provides the methods necessary for the :func:`print_report` method to properly operate. Note that each of the following methods must be implemented by your printer. Failure to do so will result in a :class:`NotImplementedError`.
        
.. function:: title(name)

Format and print the name of this report.

.. function:: section(label, name, nl)

Format and print the name of a section. ``label`` is a string which classifies ``name``, eg "Module", "Class". ``nl`` is a bool which signifies this output string should conclude with a newline.

.. function:: log_test(label, result)

Format amd print the given result of a single assert. ``label`` is a string which classifies the result, eg "Test".

.. function:: log_fixture(label, result)

Format amd print the given result of a ficture. ``label`` is a string which classifies result, eg "Before Class", "After Class".

.. function:: cleanup()

Run at the end of the report. Performs any actions needed to reset the system.


Printers
--------

The built-in printer modules.

Command Line (CLI): printers.cli
################################

The default printer. This is actually a package of 3 printers selected based on the environment in which the test is running. The goal is to produce color output to the command line. In the standard Windows console, this should always work. In Linux, it will only work in bash, due to the obnoxious method I had to use of coloring via character control codes. No matter the environment, if it is detected that I can't output in color, then I output in the same format, but black and white.

I intend to rework these using third-party modules such that color will work on Windows, Linux, and Mac, but haven't gotten around to it yet.

HTML: primaters.html
####################

Outputs to a file in HTML. Nothing is written to stdout except a success message that also prints the location the file was written to.

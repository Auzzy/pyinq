Features
========

Below is a partial list of notable features of PyInq, especially as compared to PyUnit. Note that some of the notable featurs did themself come from PyUnit.

Differences From PyUnit
-----------------------
* Test identification by decorators
* Module level tests and fixtures
* Simplified suite creation and execution
        * No calling or invoking a test runner
        * Create suites with a single keyword argument, not a separate object
* Eval functions
* Detailed, color coded output
        * For each test, prints the result of each assert and eval statement
        * Color coded based on result
* Pythonic naming

Other Notable Features
----------------------
* Test fixtures
        * Test, class, module, and suite level
* Expected exceptions
* Conditional skips
* Output to command line (CLI) or an HTML file
        * CLI defaults to color output in Windows console and Linux bash
        * CLI defaults to black and white in any other system
* Command line test module/suite execution
* Access to class instance without using self

Coming soon
-----------
* Test discovery
* Context manager for assert_raises
* Command-line single test case/class execution
* Multi-suite tests
* Custom printer modules
* Python 3 support

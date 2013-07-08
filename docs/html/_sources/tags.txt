pyinq.tags
==========
In order to support a portable and non-restrictive idenitification mechanism, PyInq makes use of Python decorators (which it refers to as tags).

In order to identify a function as a test in PyInq, the function must be wrapped with a test decorator. Similarly, classes containing tests must be wrapped with a testClass decorator.

A tag may accept arguments to modify the function's operation, such as its inclusion in a test suite. Other tags identify test fixtures, or cause the test to be skipped (either conditionally or unconditionally).

Test Identification
-------------------
.. decorator:: test([expected][,suite])
   
   Registers the function/method that follows as a test. When the containing module is run, this test is executed and its result is reported.

   All arguments must be passed as keyword arguments.

   ``expected`` signifies that this test should raise the specified error. Note that if any expression in the test raises the desired exception, the test passes. For more fine grain control over expected exceptions, see :func:`assert_raises`.

   ``suite`` should be a string indicating which suite to put this test in, which can be run from the command line (see :ref:`execution`).

.. decorator:: testClass([suite])

   Registers the class as containing tests. This allows the entire class to be skipped or added to a suite. Behavior of registered tests in an unregistered class is undefined.

   All arguments must be passed as keyword arguments.

   ``suite`` should be a string. All methods in the class will be added to the named suite, which can be run from the command line (see "Test Execution" below). Note that this includes methods listed to be included in a different suite. In this case, the test will appear in both suites.

Test Fixtures
-------------
Note that any fixtures defined outside a class treat all module scope tests as belonging to a single class.

The order of execution is:

#. beforeSuite
#. beforeModule
#. beforeClass
#. before
#. test
#. after
#. afterClass
#. afterModule
#. afterSuite

.. decorator:: before
   after

   Run before and after each individual test function. Each class may define its own before and after function. A module may define its own before and after function.

.. decorator:: beforeClass
   afterClass
   
   Run before the class's first test and after its last test. A module may define its own beforeClass and afterClass function.

.. decorator:: beforeModule
   afterModule
   
   Run before and after the containing module; that is, all tests in the module. This function should be defined in the module scope.

.. decorator:: beforeSuite([suite])
   afterSuite([suite])
   
   Run before and after the named suite. If no suite is provided, it is run only when no specific suite is run, effectively treating all detected tests as part of the same suite. This function should be defined in the module scope.

Skip
----
.. decorator:: skip
   
   Unconditionally skips the function or class.

.. decorator:: skipIf(cond)
   
   Skips the function or class only if the condition is True.

.. decorator:: skipUnless(cond)
   
   Skips the function or class only if the condition is False.

:mod:`pyinq.results`
====================

When a test is run, the results are output in a highly structured heirarchy. The heirarchy reflects the structure of the tests. Thus, there is a separate test result object for each suite, module, class, and test function. The heirachy of these objects is as expected: modules in suites, classes in modules, and tests in classes.

There is also an individual assert result object for each assert/eval function, which is contained within its corresponding test result object. The specific type of assert result object depends on which specific assert/eval function was called.

Assert Result Objects
---------------------

The following assert result objects form the base of all assert result objects.

.. class:: Result(result)
        
        The base object for all assert result objects.

        ``result`` is a three-state variable (True, False, or None) indicating the success of the call. True indicates it passed, False indicates it succeeded, and None indicates an unepxected error occurred.

.. class:: AssertResult(lineno, call, result)
        
        The base for all assert calls. Along with the result of the call, any subclass must provide the line number the call appeared on, as well as the actial call itself.
        
        As the simplest assert result object, it serves as the result for assert_true, assert_false, assert_none, assert_not_none, assert_attrib, assert_not_attrib, eval_true, eval_false, eval_none, eval_not_none, eval_attrib, and eval_not_attrib.


The following assert result objects are actually raised, and subclass :class:`AssertResult`. All of them override their calls to :func:`str` to output a very pretty mesasge containing the relevant info.

For :class:`AssertEqualsResult`, :class:`AssertInResult`, :class:`AssertInstanceResult`, the additional arguments are the parameters that were passed into the corresponding assert/eval function.

Since :class:`AssertRaisesResult` and :class:`ExpectedErrorResult` both deal with expected errors, their parameters do not directly map to their data.

.. class:: AssertEqualsResult(lineno, call, result, actual, expected)
     
        The result of a call to assert_equal, assert_not_equals, assert_is, assert_is_not, eval_equal, eval_not_equal, eval_is, or eval_is_not.

.. class:: AssertInResult(lineno, call, result, item, collection)

        The result of a call to assert_in, assert_not_in, eval_in, and eval_not_in.

.. class:: AssertInstanceResult(lineno, call, result, obj, cls)

        The result of a call to assert_is_instance, assert_is_not_instance, eval_instance, and eval_is_not_instance.

.. class:: AssertRaisesResult(lineno, call, result, trace, expected)
       
        The result of a call to assert_raises or eval_raises.
        
        Stores the traceback of the function call (if there was one) as well as the exception that was expected.        

.. class:: ExpectedErrorResult(result, expected, lineno=None)
       
        This object is not actually the result of a call to an assert function. Rather, it occurs when an error was raised somewhere in the test, and that error was marked as expected in the ``@test`` tag. Why is it underneath AssertResult, then? Because it is similar enough that it didn't make sense to separate it. That being said, I've come to the conclusion that it really shouldn't be here, so it will be moving soon.

        Contained within it are the expected error and the lineno it occurred on, if it occurred. If an error was expected but didn't occur, ``lineno`` will be :const:`None`.
        
        The value for ``call`` will always be :const:`None` since there is no explicit assert call that caused the error. I may be able to detect the line the error actually occurred on, but currently don't. While this would have some value, it would be tricky to do without making some environment assumptions. Additionally, :func:`assert_raises` allows for just this functionality.

The following assert result objects are also actually raised, but inherit directly from :class:`Result`.

.. class:: FailResult(lineno, mess)

        Occurs when :func:`fail` is called.

        The value of ``result`` will always be :const:`False`, since :func:`fail` forces the test to fail. ``lineno`` is the line that fail occurred on, and ``mess`` is the user provided message.

.. class:: UnexpectedError(trace)
        
        This is the result when an unexpected error occurs. An unexpected error is an error that is not defined by the ``@test`` tag, occurs outside of an assert_raises function, or is not defined for the current assert_raises function.

        The value of ``result`` will always be :const:`None`, to indicate an unexpected error. ``trace`` contains the traceback of the unexpected error.


Test Result Objects
-------------------

The following classes form the base for the rest of the test result objects. Note that each of them inherits from :class:`list`.

.. class:: TestResultStruct(name)
        
        The base test result class. All results inherit from this, either directly or indirectly.

.. class:: TestResultContainer()
        
        The base class for test results objects that are a collection of other test results objects, eg. :class:`TestClassResult`, :class:`TestModuleResult`, and :class:`TestSuiteResult`.


The following test result objects are directly returned when a data object is called.

.. class:: TestResult()
        
        Contains the assert result objects for each assert that was called in the corresponding test. This is the only test result object which can contain assert result objects, and in fact cannot contain other test result objects.

.. class:: TestClassResult()
        
        Contains a test result object for each test in this class. Can only contain :class:`TestResult` objects.

.. class:: TestModuleResult()
        
        Contains a test result object for each class in this module. Can only contain :class:`TestResultClass` objects.

.. class:: TestSuiteResult()
        
        Contains a test result object for each module in this suite. Can only contain :class:`TestResultModule` objects.


All of these objects except (:class:`TestResultStruct`) contain the following method.

.. function:: get_status()

        Gathers the state of all (test and assert) result objects and returns it. If any unexpected errors have occurred, the test is reported to have terminated with an error. If no unexpected errors occurred but at least one assert failed, the test is reported to have failed. If there were no unexpected errors and no failed asserts, the test passed.

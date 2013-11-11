:mod:`pyinq.asserts`
====================

Assert functions are provided by PyInq to allow the writer to evaluate the program state as needed. These functions are special, as they report their result back to the framework, which then logs the result appropriately.

PyInq provides 2 flavors of assert statements: traditional assert functions, pre-fixed with "assert"; and passive eval functions, pre-fixed with "eval". The difference between them lies in their handling of a test failure. If an assert function fails, the test ends immedaitely, any test cleanup fixtures are run, and the next test begins. If an eval function fails, the result is simply logged, and execution continues.

This suggests 2 very different uses of these functions. Asserts are for testing state that could cause unexpected behavior if it is wrong. Evals are best used to check field and variable values that need to be correct, but will not interrupt execution if they're wrong. This allows for more efficient bug fixes, as multiple minor bugs can be caught and fixed simultaneously.

Asserts/Evals
-------------

.. function:: assert_true(expr)
   assert_false(expr)
   eval_true(expr)
   eval_false(expr)

   Evaluates the truth value of expr.
   Note that the truth value is *not* the same as expr==True. For that operation, use either assert_equal(expr,True) or assert_is(expr,True).

.. function:: assert_none(expr)
   assert_not_none(expr)
   eval_none(expr)
   eval_not_none(expr)

   Evalutes whether or not expr is None.

.. function:: assert_equal(actual, expected)
   assert_not_equal(actual, expected)
   eval_equal(actual, expected)
   eval_not_equal(actual, expected)

   Test the equivalence of actual and expected. Although not enforced, actual should be the result of the expression under test and expected should be the passing value. Equivalence is determined by the == and != operators (equality by value).

.. function:: assert_is(actual, expected)
   assert_is_not(actual, expected)
   eval_is(actual, expected)
   eval_is_not(actual, expected)

   Tests whether actual and expected are the same object as determined by the is operator (equality by reference).

.. function:: assert_in(item, container)
   assert_not_in(item, container)
   eval_in(item, container)
   eval_not_in(item, container)

   Tests for membership of item in container.

.. function:: assert_is_instance(obj, cls)
   assert_is_not_instance(obj, cls)
   eval_is_instance(obj, cls)
   eval_is_not_instance(obj, cls)

   Tests whether obj is an instance of cls. Just as with isinstance, cls can be a tuple of classes.

.. function:: assert_raises(exception, func, \*args, \*\*kwargs):
   eval_raises(exception, func, \*args, \*\*kwargs):

   Executes func with the provided args and kwargs, and ensures that an exception of the provided type is raised. If an exception is raised of a different type, then the test will result in an error. If no exception occurs, the test fails.

Fail
----
.. function:: fail(mess)

   Unconditionally causes the test to fail and exit, and prints the given message.

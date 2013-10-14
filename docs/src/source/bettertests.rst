.. _better-tests:

Writing Better Tests
====================

All that's *necessary* for a unit test is a test function and assert statements. However, this will quickly lead to large, cumbersome, hard to maintain tests with a high rate of redundancy. In order for a framework to be useful, it must provide you with features that make your life easier. So although these advanced features ae not required, it is recommended that you familiarize yourself with them in order to allow yourself to write more robust tests.

Eval Functions
--------------

As useful as it is for the first assert failure to cause a test to exit, this is not always the desired behavior. Sometimes you are evaluating less critical pieces of program state. While you have an expectation for these values, an incorrect value will not lead to a problem in other parts of the test. Thus, you'd like to see these incorrect values, but only halt if a critical value is wrong.

For this, PyInq has eval functions. Evals are passive asserts. Their names and operation correspond to assert statements, but they do *not* cause the current test to halt on failure.

Take this example::

        from pyinq.tags import test
        from pyinq.asserts import eval_true

        @test
        def evals_failing():
                eval_true(False)
                eval_true(True)

The first eval will fail, since it is expecting :const:`True`. However, because it is an eval, this failure will simply be logged, and the test will continue. In this case, the second eval is run, which evaluates to :const:`True`. The test itself failed, as not all evals passed, but the second eval is still executed.

BE VERY CAREFUL WHEN USING EVALS. Since a failed eval does not halt execution, you should not use them to check critical values in the program. Doing so could cause unexpected program state, and obscure the true cause of a test failure. If in doubt as to the appropriateness of an eval, use an assert.

All eval fucntions are included in the :mod:`pyinq.asserts` package.

Mixing asserts and evals
^^^^^^^^^^^^^^^^^^^^^^^^

More often than not, there will be a mixture of important and unimportant pieces of program state. Thus, you'd like to use an assert for some conditions, and an eval for others. There is nothing preventing you from doing this.::
        
        from pyinq.tags import test
        from pyinq.asserts import eval_true,assert_true

        @test
        def mixture():
                eval_true(True)
                assert_true(True)

And to demonstrate an eval function's passive nature::
        
        from pyinq.tags import test
        from pyinq.asserts import eval_true,assert_true

        @test
        def mixture():
                eval_true(False)
                assert_true(True)

Expected Errors
---------------

Well written code should raise an error if it enters a state it cannot recover from. It is better to let the caller deal with the damage than make things worse by incorrectly "fixing" it. This is especially true of libraries, where the caller may be coming from anywhere. Plus, it adheres to one of Python's mantras: "It is easier to ask for forgiveness than permission". As such, it is necessary to check that a function that should return an error, does.

There are 2 ways to do this: the hard way, or the easy way. First, the hard way::

        from pyinq.tags import test
        from pyinq.asserts import assert_true,fail

        @test
        def expected_error_hard():
                try:
                        int("val")
                        fail("Expected a ValueError, but it didn't occur.")
                except ValueError:
                        assert_true(True)

If the expected error (:const:`ValueError`) doesn't occur, :func:`fail` is called with a message, forcing the test to immediately fail and display the message. If the expected error is raised, the except block catches it and executes. A dummy assert is run because otherwise, the test will be reported as having no asserts rather than succeeding. You could of course organize this as a helper method to make use easier, but that's beside the point. This is overly verbose, ugly, and a pain to set up and use.

Since this is a very common operation, PyInq allows you to indicate that a test should expect a certain error. If the error occurs at any point in the test, the test passes; if it fails to occur, the test fails. This is done with an argument to the :func:`test` tag::

        from pyinq.tags import test

        @test(expect=ValueError)
        def expected_error_easy():
                int("val")

The above test will pass if a :const:`ValueError` is raised, and will fail if no error is raised. Note that if ValueError is raised, the test still immediately halts; it simply reports that it passed rather than reporting the error. Also, if an error that is not the expected error is raised, it is treated as a normal error.

Considerations for expected
^^^^^^^^^^^^^^^^^^^^^^^^^^^

One important thing to note. When the expected error is raised, the test will still immediately halt; it will just do so with a report of success. But what about ensuring a specific statement raises an error? Or doing something else once that error is raised? Consider the following code, testing the user's :func:`add` function::

        from pyinq.tags import test
        
        @test(expected=TypeError)
        def false_positive():
                kwargs = dict(("num1", "2"), ("num2",8))
                add(**kwargs)

        def add(num1, num2):
                return int(num1) + int(num2)

Because they have misused the builtin :func:`dict` function, which raises a :const:`TypeError` in the case of failure, the test will pass. However, since :func:`add` would not raise an error, it seems this test should fail. On its own, the expected argument cannot handle this situation.

There are two ways to account for this situation. You could place the statement you expect to raise the error at the end of the test. In some xUnit frameworks, this is your only option. But it falls short, restricting you, while leaving some ambiguity. A statement could (correctly) raise an exception before the statement you wish to test, giving you a false positive. You will see this in the traceback, but will then have to restructure your test to account for it, which is a pain.

The other option, provided to you by PyInq (amongst other frameworks), is to use an assert specialized for this task.

assert_raises
^^^^^^^^^^^^^

The :func:`assert_raises` function allows you to ensure a specific error is raised by a specific function call. Simply pass the expected error and the function to evaluate, in that order. You may also pass a list of arguments and/or keyword arguments in the same manner as usual. PyInq runs the function with these arguments and logs the test as a success or failure based on which exception is raised, if any.

Note that it is important to pass a function to :func:`assert_raises`, not an expression. If you provide an expression, Python will evaluate and raise any errors on its own, circumventing assert_raises.

Let's re-write the above test (:func:`false_positive`) using :func:`assert_raises`::

        from pyinq.tags import test
        
        @test
        def false_positive():
                kwargs = dict(("num1", "2"), ("num2",8))
                assert_raises(TypeError, add, **kwargs)

        def add(num1, num2):
                return int(num1) + int(num2)

Since an error is no longer expected, the incorrect call to :func:`dict` will cause the test to fail with an error. Once that's corrected, the test will fail due to :func:`add` not raising an error::

        from pyinq.tags import test
        
        @test
        def false_positive():
                kwargs = dict(num1="2", num2=8)
                assert_raises(TypeError, add, **kwargs)

        def add(num1, num2):
                return int(num1) + int(num2)

This is a much more straightforward and controlled method of checking for exceptions, and as such, is the manner in which I recommend doing so.

Forcing Failure
---------------

Especially when combined with evals, assert functions are robust enough to handle many situations you'll get into while testing. However, no test framework can claim to cover every case. As such, PyUnit includes a :func:`fail` function, which let you force PyInq to fail the current test, as can be seen above. It also accepts a single string to serve as the reason for the failure. If no message is provided, a default message stating that the failure was user-initiated is instead used.

An example of both uses::

        from pyinq.tags import test
        from pyinq.asserts import fail

        @test
        def force_fail_no_message():
                fail()

        @test
        def force_fail():
                fail("This is a user-generated failure message.")

Test Fixtures
-------------

Python holds the DRY (Don't Repeat Yourself) principle very close to its heart. You should strive for code reuse wherever possible. It reduces the number of opportunities for errors, makes debugging easier, and leads to much cleaner code.

In unit testing, tests often have to initialize the program state before beginning, and should clean up after themselves once they complete. In the examples so far, that code has been a part of the test itself. This works - to a point.

It means you have code that you aren't testing as part of test. Set up code should be code you trust, either because it is guarenteed to work, or because it's tested elsewhere. Thus, having it in a test is...awkward. It isn't the focus of this test. What happens if you have clean up code that must run regardless of whether or not a test succeeds? Any time an assert fails, the test ends immediately, so this won't happen.

Additionally, it often leads to code in direct violation of DRY. Most mature test suites will have a number of related tests which all use the same set up and tear down routines. These will likely be grouped together, be it in the same file, or using one of the advanced structures yet to be described (:ref:`test_classes` and :ref:`test_suites`). What you'd really like to do is register some code with PyInq that will always be used as set up code for a group of related functions.

As with most major unit test frameworks, PyInq provides this functionality in the form of test fixtures. A test fixture marks a function as the set up or tear down function for a certain group of tests.::

        from pyinq.asserts import assert_equal,assert_true
        from pyinq.tags import before,test,after

        @before
        def setup():
                global fib
                fib = [1, 1, 2, 3, 5, 8, 13]

        @test
        def verify_fib():
                global fib
                num1, num2 = fib[:2]
                for next in fib[2:]:
                        assert_equal(num1 + num2, next)
                        num1, num2 = num2, next

        @test
        def test_ratio():
                global fib
                phi = (1 + pow(5, 0.5)) / 2
                num = fib[0]
                prev_diff = float('inf')
                for next_num in fib[1:]:
                        ratio = float(next_num) / num
                        diff = abs(phi - ratio)
                        assert_true(diff <= prev_diff)
                        num, prev_diff = next_num, diff

        @after
        def teardown():
                global fib
                del fib

The above example demonstrates the use of both basic test fixtures. :func:`setup` will occur before each test, as indicated by the :func:`before` tag. :func:`teardown` will occur after each test, as indicated by the :func:`after` tag. The test fixtures contain the common setup and tear down code, allowing each test to take care of itself. Since they occur before and after each test, :func:`before` and :func:`after` are called test-level fixtures.

If you require setup and/or tear down for an entire module, use module-level fixtures.::
        
        from pyinq.asserts import assert_equal,assert_true
        from pyinq.tags import beforeModule,test,afterModule

        @beforeModule
        def setup_module():
                global fib
                fib = [1, 1, 2, 3, 5, 8, 13]

        @test
        def verify_fib():
                global fib
                num1, num2 = fib[:2]
                for next in fib[2:]:
                        assert_equal(num1 + num2, next)
                        num1, num2 = num2, next

        @test
        def test_ratio():
                global fib
                phi = (1 + pow(5, 0.5)) / 2
                num = fib[0]
                prev_diff = float('inf')
                for next_num in fib[1:]:
                        ratio = float(next_num) / num
                        diff = abs(phi - ratio)
                        assert_true(diff <= prev_diff)
                        num, prev_diff = next_num, diff

        @afterModule
        def teardown_module():
                global fib
                del fib


:func:`setup_module` and :func:`teardown_module` will both only run once; before anything else in the module is run, and after everything else has finished running, respectively. Thus, if there is program state that will not change throughout the module, module-level fixtures can set this up.

Important notes
^^^^^^^^^^^^^^^

* If a test fails and an :func:`after` fixture is defined, that fixture *will still execute*. It is intended to reset the test environment, and so should undo any damage the test may have caused. Additionally, it should not be adverseley affected by a failed test.

* In the event that an error occurs in a fixture, how it's handled depends on if it's a 'before' or 'after' fixture.
  
  * In an 'after' function, the fixture immediately terminates,a nd execution moves on to the next test. If the next test triggers another 'after' function, it is run normally.
  * In a 'before' function, the current test will be skipped, as will any 'before' and 'after' functions below it. However, the corresponding 'after' function and any 'after functions' above it will still execute. For example, if an error occurs in a :func:`beforeModule` function, the :func:`before` fixture and :func:`after` fixture will be skipped, along with the test itself. But the :func:`afterModule` fixture will still run.

* Fixtures do not need to appear in any particular order. PyInq knows when to run each fixture based on its type, not on its physical location. You may want to keep a specific order to make it easier for you to read, but it make no difference to PyInq.

* Fixtures need not appear in pairs. :func:`before` may appear without :func:`after`, and vice versa. When it comes time to run the omitted fixture, it will simply be skipped.

* Mixing fixture types is not only allowed; it's encouraged, A file may have both test-level and module-level fixtures. However, a single module should not contain multiple fixtures of the same type (ie two functions marked with :func:`before`). In the case that this occurs, the behavior is undefined.

.. _test_classes:

Test Classes
------------

A test class is a group of functions, organized into a Python class, which will be run together. They should be grouped together for a reason, most often that they are testing the same unit in your project.

To denote a test class, decorate your class with the :func:`testClass` tag, and put your tests in it. Without this tag, the behavior of the tests within that class is undefined.

Here is a very basic test class::
       
        from pyinq.asserts import assert_true
        from pyinq.tags import testClass,test

        @testClass
        class Class1(object):
                @test
                def test_class_test_1():
                        assert_true(True)

Note something very important: as with other test functions :func:`test1` doesn't take any parameters. *Not even self*. Rather than forcing you to provide :attr:`self` to test class functions, it's created and passed to each test behind the scenes. Each test gets its own instance of :attr:`self`, so this can't be used to share values across tests.

To refer to an instance of the test class, simply use the attribute :attr:`self`, as you would in a normal Python class.::

        from pyinq.asserts import assert_equal
        from pyinq.tags import testClass,test

        @testClass
        class Class1(object):
                @test
                def using_self():
                        self.num = 8
                        assert_equal(self.num,8)

In the context of a lone test, :attr:`self` is not very useful. But when combined with test-level fixtures, it's utility becomes clear::

        from pyinq.asserts import assert_equal
        from pyinq.tags import testClass,before,test

        @testClass
        class Class1(object):
                @before
                def setup():
                        self.num = 4
                
                @test
                def using_self():
                        assert_in(self.num,4)

Although a contrived example, this shows a couple very important things. First off, in the context of a test class, test-level fixtures also are passed :attr:`self` by PyInq behind the scenes (this includes :func:`after`, although it's not shown here). Secondly, :attr:`self` represents an instance of the test class, which is maintained throughout the life of the test. As such, local variables can be set which are inaccessible from any other test.

In many instances, you will not need this feature, but it can be useful nonetheless.

Test Class Fixtures
^^^^^^^^^^^^^^^^^^^

A class-level test fixture is a function in a test class marked with either the :func:`beforeClass` or :func:`afterClass` tag. These fixtures run before and after everything else in the class::

        from pyinq.asserts import assert_in
        from pyinq.tags import testClass,beforeClass,test,afterClass

        @testClass
        class Class1(object):
                @beforeClass
                def setup_class():
                        Class1.nums = [1,1,2,3,5,8,13,21]
                
                @test
                def using_self():
                        assert_in(8,Class1.nums)

                @afterClass
                def teardown_class():
                        del Class1.nums
 
Note that class-level fixtures *are not part of a class instance*. They are executed as static methods of the class that contains them. As such, they do *not* have access to :attr:`self`.

.. _test_suites:

Test Suites
-----------

A test suite is a group of tests that are executed together. They may or may not have any logical connection, and they are not necessarily collected in one module.

By default, all tests are in the same, unnamed suite; that's why they all run together. However, you can explicitly define a test as part of a suite. No matter where the test is located in the file, its suite memebership will be logged.

A test that is part of a suite will still be run by default. Being in a suite simply means that all specified tests will be run when that suite is run.

Tests
^^^^^

Any PyInq test may be made part of any test suite. All it requires is an argument to the :func:`test` tag::
        
        from pyinq.asserts import assert_true
        from pyinq.tags import test

        @test(suite="suite1")
        def suite_test1():
                assert_true(True)

        @test(suite="suite2")
        def suite_test2():
                assert_true(True)

        @test(suite="suite1")
        def suite_test3():
                assert_true(True)

        @test
        def suite_test4():
                assert_true(True)

In the above example, 2 new suites are created: "suite1" which contains :func:`suite_test1` and :func:`suite_test3`; and "suite2" which has :func:`suite_test2`. Note that no setup is required to make a test suite. Simply provide the name of the suite as a string: if it already exists, the test will be added to the correct suite; otherwise, the suite is created. This example also demonstrates mixing tests not in a suite with ones that are.

Class tests may also be part of a suite::

        from pyinq.asserts import assert_true
        from pyinq.tags import testClass,before,test
        
        @testClass
        class Class1(object):
                @before
                def setup():
                        assert_true(True)

                @test(suite="suite1")
                def test1():
                        assert_true(True)
                
        @before
        def setup():
                assert_true(True)

        @test(suite="suite1")
        def test2():
                assert_true(True)

When "suite1" is executed, both test1 and test2 will be executed. *This includes any relevant test fixtures*. In the above, :func:`Class1.setup` will be run before :func:`Class1.test1`, and :func:`setup` will be run before :func:`test2`, although neither fixture is tagged as part of the suite. The same goes for test fixtures of any level. PyInq assumes that these test fixtures contain code necessary for the associates tests to run, so it wouldn't make sense to leave them out of the suite.

Test Classes
^^^^^^^^^^^^

An entire test class may be made part of a test suite in much the same way as a test::

        from pyinq.asserts import assert_true
        from pyinq.tags import testClass,test
        
        @testClass(suite="class suite")
        class Class1(object):
                @test(suite="suite1")
                def test1():
                        assert_true(True)

                @test
                def test2():
                        assert_true(True)

When the ``suite`` argument is passed to :func:`testClass`, every test in the class is added to the named suite. If a test specifies its own suite, it is added to both. Thus, in the above example, :func:`Class1.test1` appears in both "suite1" and "class suite", while :func:`Class1.test2` only appears in "class suite".

Test Suite Fixtures
^^^^^^^^^^^^^^^^^^^

Test suites also have their own set of test fixtures, which are predictably named :func:`beforeSuite` and :func:`afterSuite`. They're associated with the appropriate test suite by an argument naming the suite, since suites don't have a central location::

        from pyinq.asserts import assert_true
        from pyinq.tags import beforeSuite,test
        
        @beforeSuite(suite="suite1")
        def setup_suite1():
                assert_true(True)
        
        @beforeSuite
        def setup_default_suite():
                assert_true(True)
        
        @test(suite="suite1")
        def test1():
                assert_true(True)

        @test
        def test2():
                assert_true(True)

You'll notice that :func:`setup_default_suite` is not told which suite to setup. This indicates it should setup the deafult suite. Thus, :func:`setup_default_suite` is the default suite's "before" fixture, and :func:`setup_suite1` is the "before" fixture for "suite1".

Skipping Tests
--------------

There are a number of reasons you may wish to not run a test. Sometimes you know it fails but haven't had time to fix it, and sometimes it's incomplete. To this end, PyInq provides a simple method for skipping the test without having to change anything about the test itself::

        from pyinq.asserts import assert_true
        from pyinq.tags import test,skip

        @skip
        @test
        def test1():
                assert_true(True)

With the simple addition of the :func:`skip` tag, the test will be passed over. To reinsert it, simply delete the tag.

If you attempt to run a module (or suite) in which all tests are marked to be skipped, that is in fact what will happen: no tests will be run, and thus no report will be printed.

Conditional Skips
^^^^^^^^^^^^^^^^^

Some tests only apply in certain cases. For example, you may have cross-platform software, which implies some tests will only make sense on one platform. You also could have a new API function, so tests that use it should only be run if the most up to date API is being tested. PyInq makes this an easy problem to solve with :func:`skipIf` and :func:`skipUnless`::

        import platform
        import os

        from pyinq.asserts import assert_false,assert_equal
        from pyinq.tags import test,skipif,skipUnless

        @test
        @skipUnless(platform.system() == "Unix")
        def test_Unix():
                assert_equal(os.getlogin(),os.environ["LOGNAME"])

        @test
        @skipIf(platform.python_version_tuple() < (2,3))
        def test_unicode_filenames():
                from os.path import supports_unicode_filenames
                assert_false(supports_unicode_filenames)

Both :func:`skipIf` and :func:`skipUnless` accept a single argument which should be some test for whether or not to run the test. A test decorated with :func:`skipIf` will *only* be skipped if this result is :const:`True`, while a test decorated with :func:`skipUnless` *will* be skipped UNLESS the result is :const:`True`. In the above example, :func:`test_Unix` will be skipped unless the test is being run on a Unix system. :func:`test_unicode_filenames` will not be run if the Python version is less than 2.3, as that was when the function was added.

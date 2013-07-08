Getting Started
===============

Any module that imports from the pyinq package is treated as a PyInq test module upon load. Thus, upon running the module, all tests in the file will be picked up and executed according to the command line options provided.

Your First Test
---------------

Writting a test is very simple. In PyInq, a test is just a function that is decorated with the ``@test`` tag::
        
        from pyinq.tags import test

        @test
        def my_first_test():
                pass

Note that the test function does not have any parameters. A PyInq test must not take any parameters.

PyInq includes a number of tags for different operations, all of which are included in :mod:`pyinq.tags`.

Writing Useful Tests
--------------------

If you run the above test, you'll notice it doesn't actually do anything. Some output is produced, including a report on :func:`my_first_test` which informs you it contains no asserts. While this isn't a problem for PyInq, it probably isn't what you wanted. You probably wanted to run some of your code, then check that the correct values were affected. You wanted assert functions!

Assert Functions
^^^^^^^^^^^^^^^^

To begin, let's add an assert!::
        
        from pyinq.tags import test
        from pyinq.asserts import assert_true

        @test
        def single_assert():
                assert_true(True)

The above is a use of the most basic assert function. Its only argument is a Python expression. If the expression has a truth value of :const:`True`, it passes; otherwise, it fails. Since its argument is the boolean value :const:`True`, the above test will pass.

Upon execution, you will see a brief report on this test, including a status indicating it passed. This is because all asserts in the test passed. If a single assert fails, the test fails. Additionally, for each assert you will see a line indicating its success, as in the following example::
        
        from pyinq.tags import test
        from pyinq.asserts import assert_true,assert_false

        @test
        def two_asserts():
                assert_true(True)
                assert_false(False)

Both tests pass, so the test itself passes. Also, we once again see a line for each assert function call in test report.

All assert fucntions are included in the :mod:`pyinq.asserts` package.

Test Contents
^^^^^^^^^^^^^

Clearly, the examples so far have been incredibly simple, and if you are unfamiliar with unit testing, they may have left you wondering what the point is. So before I go any further, let me give you a more realistic (albeit simple) example using a function built in to Python::
        
        import random
        from pyinq.tags import test
        from pyinq.asserts import assert_in,assert_equal,assert_not_equal

        @test
        def shuffle_test():
                seq = range(0,10)
                shuffled = random.shuffle(seq)
                assert_not_equal(seq,shuffled)
                assert_equal(len(seq),len(suffled))
                for item in shuffled:
                        assert_in(item,seq)

In the above test, the :func:`random.shuffle` function is being tested. If the sequence is shuffled, then it should not be equal to the original sequence, although their lengths should be equivalent. Additionally, all items in the shuffled sequence should be present in the original sequence. This guarantees the shuffled sequence has the exact same contents as the original sequence (no more and no less), but they do not appear in the same order.

Assert Failure
^^^^^^^^^^^^^^

All of the previous examples are set up such that the asserts will indeed pass. But what happens when an assert fails?::

        from pyinq.tags import test
        from pyinq.asserts import assert_true

        @test
        def failing_assert():
                assert_true(False)

The test status is reported as failed, and the assert function call is also reported as failed. Given the behavior when an assert passes, this is not surprising.

But what if a test contains multiple asserts?::

        from pyinq.tags import test
        from pyinq.asserts import assert_true

        @test
        def asserts_failing():
                assert_true(False)
                assert_true(True)

Note that only the first assert statement is listed in the report. The second assert's output is not displayed. This is because the second assert *is not executed*. This exposes a key feature of assert statements; a failed assert causes the current test to halt. This can be an incredibly useful detail. It means that following an assert, you may assume that expression is true until an object in the expression is modified. If the condition wasn't true, then the test would have ended.

For example, in the following test it is first asserted that the variable :data:`foo` is a string, then that it contains only alphabetic characters. After the first assert, there is no need to check that :data:`foo` is a string. Since the test is still running, and :data:`foo` hasn't been modified, foo must be a string, so we can safely operate on it as such::

        from pyinq.tags import test
        from pyinq.asserts import assert_true,assert_is_instance

        @test
        def test_assert():
                foo = "hello"
                assert_is_instance(foo,str)
                assert_true(foo.isalpha())

Errors
^^^^^^

Sometimes you will execute code which will raise an error. It may be unexepected, such as errors caused by an issue during file I/O. They may be expected, such as with a StopIteration error. But either way, errors will occur, and PyInq must deal with it.

When an error is raised, PyInq first checks if that error was expected (this will be discussed in detail in :ref:`better-tests`). If so, it will be handled in the appropriate manner. If it is unexpected, PyInq will log the error (including traceback) and halt the test. This way, the test will not produce any false results by attempting to continue, and all the information about the error is available to you for correction. A test which terminated due to an error will be be given a status indicating as much.

What Else?
----------

That covers all the basics of unit testing. You could do all of your testing using just what you've learned in this short document.

But that would be silly! For all but the smallest projects, your tests would quickly get large and unmanageable, full of redundant and verbose code. Luckily, PyInq provides you with many more features to ease your coding and clean up your tests. Check out the :ref:`better-tests` guide for a walkthrough of PyInq's more advanced features.

.. _discovery:

Test Discovery
==============

When testing a large project, organization is key. Grouping related tests is a faily common-sense approach, which PyInq lets you do through :ref:`test classes <test_classes>` and :ref:`test suites <test_suites>`. Additionally, you can create multiple tests files. This is a common practice, and often the test directory is constructed to mirror your source directory. Each test file corresponds to a source file, and each test directory corresponds to a source directory.

Following this convention, your test directory will look something like this::

        test_dir/
                test_foo.py
                test_bar.py
                baz/
                        __init__.py
                        test_food_bar.py
                        test_bar_food.py


While this is great for organizational purposes, it raises one *big* hurdle: you must run your test files individually. You could write a script of your own to do this for you, but you'd have to keep updating it. You could write a script to discover and execute all your tests for you, but that seems like it's something you shouldn't have to do.

And I agree.

Discovering Tests
-----------------

Running each test in the above directory is made very simple with test discovery::

        python -m pyinq discover test_dir

The "discover" keyword is what invokes test discovery, and the next argument ("test_dir" above) tells PyInq what the root test directory is. Note that it is interpreted relative to your current working directory. Thus, the above command will work if your current working directory comntains "test_dir". If you want to run discovery on the current folder (such as from within "test_dir"), replace "test_dir" with ".".

For a more detailed discussion of the options to this command, see :ref:`execute_discovery`.

How does it work?
-----------------

It's magic!

Okay, not really. However, it *is* magic in the sense that all you must do is ensure any subfolders are valid Python packages, which should be the case anyways. Remember, all that means is that the folder has a file called __init__.py, which will usually be empty. That's it. There is no directive, line of code, or anything you must add to your tests to make them discoverable.

When you run test discovery, PyInq searches the provided test directory for PyInq tests and loads them [#]_ . If it encounters a directory which appears to be a Python package, it will also search that directory for tests. If it doesn't appear to be a Python package, it will be skipped. Once this process completes, all discovered tests are executed. As with executing an individual file, the order of execution is undefined, so all tests should be independent. And of course, a report on all the test results is provided.

.. [#] PyInq imports any file matching the provided pattern (or all files if no pattern is provided), registering any tests it finds. Thus, any code not within a class or function will run at that time. For this reason, it is recommended that you avoid code outside of classes and functions.

Test Discovery API
------------------

PyInq provides an API enabling you to programmatically gather tests. It returns an object representing the suite of tests found, which you may either run or inspect for more information. Running it returns an object representing the result of each test executed, which you may either pass to a printer object for output and formatting or inspect for more information.

This is more or less how PyInq performs test discovery::
        
        import tags
        import printers

        suite_name = "foo"

        discover_tests_api(root, pattern=".*", suite_name=None)
        suite = discover_tests('examples'))
        suite = tags.get_suite(suite_name)
        if suite:
                report = suite()
                printers.print_report(report, printers.cli)

Let's walk through what's going on in the above code.

Retrieving a test suite
#######################

The first step is to retrieve the tests to be 

Running a test suite
####################


Printing a report
#################



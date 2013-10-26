.. _discovery:

Test Discovery
==============

When testing a large project, organization is key. Grouping related tests is a faily common-sense approach, which PyInq lets you do through :ref:`test classes <test_classes>` and :ref:`test suites <test_suites>`. Additionally, you can create multiple test files. This is a common practice, and often the test directory is constructed to mirror your source directory. Each test file corresponds to a source file, and each test directory corresponds to a source directory.

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

The ``discover`` keyword is what invokes test discovery, and the next argument tells PyInq where to find the root test directory. This path can be either relative or absolute. If you want to treat the current folder as the test root, make this argument ``.``.

You may also specify the filename pattern and output format. For a more detailed discussion of these options, see :ref:`execute_discovery`.

How does it work?
-----------------

It's magic!

Okay, not really. However, it *is* magic in the sense that all you must do is ensure any subfolders are valid Python packages, which should be the case anyways. Remember, all that means is that the folder has a file called ``__init__.py``, which will often be empty. That's it. There is no directive, line of code, or anything you must add to your tests to make them discoverable.

When you run test discovery, PyInq searches the provided test directory for PyInq tests and loads them [#]_. If it encounters a directory which appears to be a Python package, it will also search that directory for tests. If it doesn't appear to be a Python package, it will be skipped. Once this process completes, all discovered tests are executed. As with executing an individual file, the order of execution is undefined, so all tests should be independent. And of course, a report on all the test results is provided.

.. [#] PyInq imports any file matching the provided pattern (or all files if no pattern is provided), registering any tests it finds. Thus, any code not within a class or function will run at that time. For this reason, it is recommended (but not required) that you avoid code outside of classes and functions.

Test Discovery API
------------------

PyInq provides an API enabling you to programmatically gather tests. It returns an object representing the suite of tests found, which you may either run or inspect for more information. Running it returns an object representing the result of each test executed, which you may either pass to a printer object for output and formatting or inspect for more information.

This is more or less how PyInq performs test discovery::
        
        from pyinq import discover_tests, printers

        if __name__=="__main__":
                suite = discover_tests(root, pattern, suite_name)
                report = suite()
                printers.print_report(report, printers.cli)

This breaks down into 3 main tasks, as can be seen from the 3 separate function calls. Let's walk through what's going on in the above code.

Retrieving a test suite
^^^^^^^^^^^^^^^^^^^^^^^

The first step is to retrieve the desired tests. This is encapsulated in the ``discover_tests`` function. It takes the same arguments as the command line version. Each argument is optional. Omitting the root will start discovery in the current working directory, omitting the pattern will match all PyInq test files, and omitting the suite name will grab all PyInq tests.

In PyInq, tests have a clear heirarchy::

        suites
            modules
                classes
                    tests

As such, the objects that represent these structures also have a clear heirarchy::

        TestSuiteData
            TestModuleData
                TestClassData
                    TestData

Each object contains some data about the structure it represents, such as its name and any associated fixtures. It also consists of a list of objects from the level below (except for :class:`TestData`). That is, a :class:`TestSuiteData` object is a list of :class:`TestModuleData` objects, and so on. In this way, information about your test structure is preserved, allowing you more flexibility in how you handle these tests. The :ref:`discover_tests` function will always return a :class:`TestSuiteData` object.

Note that internally, PyInq always creates this heirarchy, even if you didn't use these structures. For example, you may have a test module that contains a bunch of tests, some of which are *not* in classes. Internally, those tests are gathered into a single, nameless class. That class's ``name`` field will be ``None`` to reflect this fact. The same is true for tests that aren't placed in any explicit test suite. They are pulled into the default test suite, which has a name of ``None``.

This makes for greater consistency and eases execution and report handling. Also, leaving the ``name`` field with a value of ``None`` allows auto-generated structures to be easily distinguished from your defined structures. Finally, it allows ``discover_tests`` to always safely return a :class:`TestSuiteData` object.

Running a test suite
^^^^^^^^^^^^^^^^^^^^

Checking that the test suite is not empty is unncessary, as PyInq will not complain. But if you do wish to check, remember that each object is just a list. Thus, Python's truth value check still works, as does explicitly checking its length.

All data objects are callable, meaning that running it is done by invoking it as you would a function. In the above code snippet, this is done by the following line::

        report = suite()

This will cause all fixtures and tests contained in the heirarchy to be executed. Running the top-level :class:`TestSuiteData` object will return a :class:`TestSuiteResult` object, which contains information on the executed tests. The information is maintained in the same heirarchical fashion in which it was consumed. There will be a 1:1 mapping from data objects to test result objects.

Manually executing a suite
##########################

Although the example shows a suite, any data object may be executed. For example, if you had a :class:`TestSuiteData` object ``suite`` and wanted to manually run each module, but not the suite itself::
         
        results = [module() for module in suite]

This will produce a list of :class:`TestModuleResult` objects. The fixtures associated with each module will be run, as will all contained test structures. Note that the suite's fixtures **will NOT be run**. Thus, tests that rely on those fixtures will likely behave unexpectedly. In order to manually run the fixtures properly, a little more work is needed::

        import pyinq.runner as runner

        result = []
        before_result,halt = runner.run_fixture(suite.before)
        if not halt:
                results = [module() for module in suite]
        after_result,halt = runner.run_fixture(suite.after)

Note the use of the special method ``run_fixture``. It is used for a few reasons. First off, it allows proper handling of any errors or asserts that may appear in a fixture. This includes returning a report on the success of any included asserts. Secondly, it allows the fixture to signal the test to stop, such as in the case of a failed assert.

I've realized this process is a bit uglier than necessary. As such, although I don't expect this to be a common use-case, I plan to clean it up in coming versions.

Manually processing a suite
###########################

Another reason for manually iterating through suites in a test is gathering the included information. For example, you may just want to print out a snapshot of the gathered tests before running them. Take this example, where the structure of the discovered tests is printed out, along with the structure's name and suite::

        from pyinq import discover_tests

        if __name__=="__main__":
                suite = discover_tests(root)
                print "SUITE: " + str(suite.name)
                for module in suite:
                        print "\tMODULE: " + str(module.name)
                        for cls in module:
                                print "\t\tCLASS: {cls.name} (SUITE: {cls.suite})".format(cls=cls)
                                for test in cls:
                                        print "\t\t\tTEST: {test.name} (SUITE: {test.suite})".format(test=test)

Note that this snippet does not actually run the tests, but merely demonstrates inspecting them.

Printing a report
^^^^^^^^^^^^^^^^^

Running your tests will produce a test results object (such as :class:`TestSuiteResult`) which contains the result of each assert or eval within each executed test. As with the data objects, these objects may be fed into functions predefined by PyInq, or you may pick them apart on your own. As with the data objects, the test result objects are lists, and thus can be iterated over.

Of course, using predefined printers is the easiest::
        
        from pyinq import printers

        printers.print_report(report, printers.cli.default)

This will print the report to the command line using the ``Printer`` class contained within the ``printers.cli.default`` module. You can also define printers to be a bit more clever using packages and the ``__init__.py`` file. For example, the printer used in our original example (``printers.cli``) is actually a package that attempts to select a printer based off the system detected so that it can display the output in color. The only requirement is that the provided namespace contains a class called ``Printer`` which inherits from :class:`AbstractPrinter`.

Constructing your own printer
#############################

If one of the included printers doesn't meet your needs, you may wish to write your own. To do so, create a class that subclasses the abstract class :class:`pyinq.printer.AbstractPrinter <AbstractPrinter>`. For now, this class must be called "Printer" to be recognized, but that will change in coming versions.

There are 4 functions to implement: ``title``, to format the report banner;  ``section``, to format the name of each section (module name, class name, etc); ``log_test``, to log the test results; and ``log_fixture``, to log the fixture results. There is also an optional ``cleanup`` function if your printer needs to perform any operations upon exiting.

To use your printer, pass the module that contains it to the ``pyinq.printers.print_report`` function, and PyInq will handle the rest!

Manually printing a report
##########################

It is possible that the default structure does not fit your needs, in which case you are left with the option to manually inspect the test results objects.

As with the data objects (discussed above), test results objects are organized into a heirarchy. When you execute a data object, you will always be given back a test results o bject of the corresponding type::

        TestSuiteData   -> TestSuiteResult
        TestModuleData  -> TestModuleResult
        TestClassData   -> TestClassResult
        TestData        -> TestResult

As mentioned above, each of these 4 classes is a list of result objects. Each result object represents the result of a single assert. All these results combine to form the outcome of the test. The outcome can be determined by calling `get_status`. Note that this methos can return 3 different values: :const:`True` if the test passed; :const:`False` if the test failed; or :const:`None` if an unexpected error occurred. An error is unexpected if it occurs outside an assert_raises statement and method expecting an error, or if the error raised is not the appropriate type.

These objects also have 3 fields. The `name` field contains the name of the test method. The other 2 fields, `before` and `after`, contain the result of the before and after fixtures at the given level. 

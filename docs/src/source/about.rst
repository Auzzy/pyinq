About PyInq
===========

PyInq was initially written for a masters course on developer testing. We had to write our own unit testing framework, and I wrote one for Python. Although little of that original code remains, it's success and ease of use inspired me to redesign and greatly extend its functionality.

What's with the name?
---------------------

`It's quite unexpected... <https://www.youtube.com/watch?v=S-O58Dqdky8>`_

What about PyUnit (unittest)?
-----------------------------

PyUnit is a well established and fairly extensive unit test framework. It has become the default for Pythonistas, partially due to some neat features, and partially due to its inclusion in the standard library.

That being said, there are some aspects of PyUnit that bother me. Imposing a naming convention on tests for identification purposes feels brittle. The requirement of you to manually create test suite objects and invoke a the test runner is unnecessary. And the whole framework feels very...un-pythonic. While some Python features and conventions are used very well, such as a context manager for assertRaises, others aren't. The camel casing of assert names and the requirment for all tests to be in a class are the most obvious offenders. In many ways, it feels like a port of JUnit, rather than an xUnit framework for Python.

Combine these issues with some ideas I already had kicking around and the existing codebase from my course assignment, and the desire and base for PyInq was in place. A number of features were based off PyUnit, and even more are coming down the pipeline. I want PyInq to become an alternative to PyUnit. To that end, I have implemented a number of features present in PyUnit, albeit with modifications to ensure their smooth integration. PyInq is designed with extension in mind, so that modofication of its operation will not be difficult for those who wish to hack on it. And even more command line options are in the pipeline to allow further control over execution.

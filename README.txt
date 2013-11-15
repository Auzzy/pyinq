=====
PyInq
=====

*Find the Spanish translation of this page here:* http://www.webhostinghub.com/support/es/misc/estructura-de-pruebas-pyinq

PyInq is a Python unit testing framework created in the tradition of the xUnit family. Specifically, it draws its influence from JUnit and PyUnit (unittest).

The bulk of PyInq's functionality was influenced by PyUnit. However, Java coders will recogize the use of decorators for test identification from JUnit 4. Selenium users will recogize PyInq's suite of "eval" functions; they were influenced by Selenium's "verify" functions.

Differences From PyUnit (unittest)
----------------------------------
* Test identification by decorators
* Module level tests
* Suite support
	* Simplified creation and execution
	* No calling or invoking a test runner
	* Create suites with a single keyword argument, not a separate object
* Eval functions (passive asserts)
* Detailed, color coded output
	* For each test, prints the result of each assert and eval statement
	* Color coded based on result
* Pythonic naming

Other Notable Features
----------------------
* Test discovery
* Test fixtures
	* At test, class, module, and suite level
* Expected exceptions
* Conditional skips
* Output to command line (CLI) or an HTML file
	* CLI defaults to color output in Windows console and Linux bash
	* CLI defaults to black and white in any other system
* Command line test module/suite execution

Documentation
-------------
Formal documentation is finally complete! It is both included in the package itself, and present on PyPI at `http://pythonhosted.org/PyInq/ <http://pythonhosted.org/PyInq/>`_. From now on, I'll be keeping this up to date as needed.

Let me know your thoughts! If you find any issues with it, feel free to email me, and I'll fix it asap.

Additionally, below I've included some examples of how to use PyInq.

##############
Basic Examples
##############
Simply run the code as is to try any of these examples for youself

A single module level test::

	from pyinq.asserts import *
	from pyinq.tags import *
	
	@test
	def atest():
		assert_true(True)

Test expecting an error::
	
	from pyinq.asserts import *
	from pyinq.tags import *
	
	@test(expected=ValueError)
	def tester():
		assert_equal(int("4.0"),4)

Using an instance variable::

	from pyinq.asserts import *
	from pyinq.tags import *
	
	@testClass
	class Class1:
		@before
		def setup():
			this.num = 4

		@test
		def test():
			assert_equal(this.num,4)
			this.num += 1
		
		@after
		def teardown():
			assert_equal(this.num,5)

unittest basic example::

	from pyinq.asserts import *
	from pyinq.tags import *
	import random

	@testClass
	class TestSequenceFunctions:
		@before
		def setUp():
			this.seq = range(10)

		@test
		def test_shuffle():
			# make sure the shuffled TestSequenceFunctions.sequence does not lose any elements
			random.shuffle(this.seq)
			this.seq.sort()
			assert_equal(this.seq, range(10))

			# should raise an exception for an immutable TestSequenceFunctions.sequence
			assert_raises(TypeError, random.shuffle, (1,2,3))

		@test
		def test_choice():
			element = random.choice(this.seq)
			assert_true(element in this.seq)

		@test
		def test_sample():
			assert_raises(ValueError, random.sample, this.seq, 20)
			for element in random.sample(this.seq, 5):
				assert_in(element,this.seq)

##############
Test Discovery
##############
Test discovery is a method for finding tests beginning at a specific root folder. The program will walk down each Python package in the folder structure until it has nowhere else to go. If any files in the package contain PyInq tests, they will be properly detected and executed.

The main way to use it is invocation from the command line, like so::

	python -m pyinq discovery <root>

Output is the same as when executing a single file, with the addition of a tag indicating which module a set of tests belongs to.

You may also choose to invoke test discovery via the API. If you do, you will be given a TestSuite object, which is executable. A sample of how to use it appears below::

	from pyinq import discover_tests
	
	suite = discover_tests('examples')
	if suite:
		suite()


Contact Me
----------
If you have any questions or comments, find any bugs, or wish to make any feature requests, shoot me an email at pyinq.test@gmail.com. I am especially hoping to receive bug reports, for although I am unaware of any bugs, fresh sets of eyes have a better chance of finding what I missed.

Also, I will be setting up a separate web page and public GitHub repo for this project very soon. I will post those links here once they are ready.

Change Log
----------
v0.2.1, November 15, 2013
    - Wrote formal documentation
    - Cleaned up a bunch of naming and heriarchical decisions
    - Refactored some ugly pieces of backend code

v0.2.0, March 3, 2013
    - Test discovery (command line and API)
    - Made test discovery a subcommand, with its own special command line arguments
    - Test execution through Python interpreter ("python -m pyinq")
    - Implicit class instance now "self" (was "this")
    - @test's expected error argument now "expect" (was "expected")
    - Empty classes no longer listed in test report

    - Disable auto-execution in code
    - Refactored test fixture and test data classes
        - Treating test object as a string yields test structure within that object
    - Rebuilt suite collection
    - Rebuilt test registration

v0.1.1, July 26, 2012 --
    - Renamed each tag to begin with a lower case letter.
    - Fixed a bug in the eval example.

v0.1.0, July 23, 2012 -- Initial release.

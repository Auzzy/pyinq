=====
PyInq
=====

PyInq is a Python unit testing framework created in the tradition of the xUnit family. Specifically, it draws its influence from JUnit and PyUnit (unittest).

The bulk of PyInq's functionality was influenced by PyUnit. However, Java coders will recogize the use of decorators for test identification from JUnit 4. Selenium users will recogize PyInq's suite of "eval" functions; they were influenced by Selenium's "verify" functions.

Differences From PyUnit (unittest)
----------------------------------
* Test identification by decorators
* Module level tests
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
	* At test, class, module, and suite level
* Expected exceptions
* Conditional skips
* Output to command line (CLI) or an HTML file
	* CLI defaults to color output in Windows console and Linux bash
	* CLI defaults to black and white in any other system
* Command line test module/suite execution

Coming soon
-----------
* Test discovery
* Context manager for assertRaises
* Command-line single test case/class execution
* Multi-suite tests
* Custom printer modules
* Python 3 support

Documentation
-------------
I have not yet had the chance to write up much documentation. It's high on my TODO list as undocumented projects can be aggrevating to work with. I intend to produce a basic guide to using PyInq, as well as code comments and docstrings.

For now, there is basic documentation in the download. In the docs folder, there is a file called "reference.txt". This assumes knowledge of unit test frameworks, and serves as a basic reference for what PyInq includes, and how to use it. The other is a directory called examples, which contains a number of tests that exercise various aspects of PyInq. I've tried to name them in a straightforward manner to enable them to giude your usage of this package.


Basic Examples
--------------
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

Contact Me
----------
If you have any questions or comments, find any bugs, or wish to make any feature requests, shoot me an email at `pyinq.test@gmail.com<mailto:pyinq.test@gmail.com>`_. I am especially hoping to receive bug reports, for although I am unaware of any bugs, fresh sets of eyes have a better chance of finding what I missed.

Also, I will be setting up a separate web page and public GitHub repo for this project very soon. I will post those links here once they are ready.

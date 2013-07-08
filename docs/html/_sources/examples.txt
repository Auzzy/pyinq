Examples
========

The following are some code snippets to show basic usage of PyInq's features.

Base (module level test)
------------------------

::

	from pyinq.asserts import *
	from pyinq.tags import *
	
	@test
	def atest():
		assert_true(True)

Eval
----

::

	from pyinq.asserts import *
	from pyinq.tags import *
	
	@test
	def atest():
		eval_false(True)
		eval_true(True)

Expecting error
---------------

::
	
	from pyinq.asserts import *
	from pyinq.tags import *
	
	@test(expected=ValueError)
	def tester():
		assert_equal(int("4.0"),4)

Suites
------

::
	
        from pyinq.asserts import *
        from pyinq.tags import *
        
        @test(suite="suite1")
        def atest():
                assert_true(True)
        
        @test(suite="suite2")
        def atest():
                assert_true(True)
        
        @test
        def atest():
                assert_true(True)

Class level test
----------------

::

	from pyinq.asserts import *
	from pyinq.tags import *
	
	@testClass
	class Class1:
		@test
		def test():
			assert_true(True)

Fixtures
--------

::

	from pyinq.asserts import *
	from pyinq.tags import *

	@testClass
	class Class1:
		@beforeClass
		def setupClass():
			assert_true(True)

		@before
		def setUp():
			assert_false(False)

		@test
		def test1():
			assert_true(True)

		@after
		def tearDown():
			assert_none(None)
	
	@testClass
	class Class2(object):
		@test
		def test2():
			assert_not_none(1)

	@beforeModule
	def setupModule():
		assert_true(True)
	
	@afterModule
	def teardownModule():
		assert_true(True)

Instance variable
-----------------

::

	from pyinq.asserts import *
	from pyinq.tags import *
	
	@testClass
	class Class1:
		@before
		def setup():
			self.num = 4

		@test
		def test():
			assert_equal(self.num,4)
			self.num += 1
		
		@after
		def teardown():
			assert_equal(self.num,5)

Skipping
--------

::
	
	import sys
	from pyinq.asserts import *
	from pyinq.tags import *
	
	@skip
	def skip_test():
		fail("Test shouldn't fire.")

	@skipUnless(sys.platform.startswith("win"))
	def windows_test():
		assert_true(sys.platform,"win32"))
			
PyUnit basic example
--------------------

::

	from pyinq.asserts import *
	from pyinq.tags import *
	import random

	@testClass
	class TestSequenceFunctions:
		@before
		def setUp():
			self.seq = range(10)

		@test
		def test_shuffle():
			# make sure the shuffled TestSequenceFunctions.sequence does not lose any elements
			random.shuffle(self.seq)
			self.seq.sort()
			assert_equal(self.seq, range(10))

			# should raise an exception for an immutable TestSequenceFunctions.sequence
			assert_raises(TypeError, random.shuffle, (1,2,3))

		@test
		def test_choice():
			element = random.choice(self.seq)
			assert_in(element,self.seq)

		@test
		def test_sample():
			assert_raises(ValueError, random.sample, self.seq, 20)
			for element in random.sample(self.seq, 5):
				assert_in(element,self.seq)

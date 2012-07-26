from pyinq.tags import *
from pyinq.asserts import *

@testClass
@skip
class Test1(object):
	@BeforeClass
	def init():
		eval_true(False)

	@test
	def test1():
		assert False
	
@skip
@testClass
class Test2:
	@BeforeClass
	def init():
		eval_true(False)
	
	@test
	def test2():
		assert False

@skip
@testClass
class Test3(object):
	@test(suite="suite1")
	def test5():
		assert_true(False)
	
	@test(suite="suite1")
	def test3():
		assert_true(False)

@skip
@testClass
class Test4(object):
	@test(suite="suite1")
	def test4():
		assert_true(False)

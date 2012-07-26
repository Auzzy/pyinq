from pyinq.tags import *

@testClass(suite="suite1")
class Class1(object):
	@test
	def test1():
		assert True
	
	@test
	def test2():
		assert True

@testClass(suite="suite2")
class Class2(object):
	@test(suite="suite1")
	def test3():
		assert True
	
	@test(suite="suite2")
	def test4():
		assert True

@testClass
class Class3(object):
	@test
	def test5():
		assert True
	
	@test
	def test6():
		assert True

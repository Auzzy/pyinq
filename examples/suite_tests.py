from pyinq.tags import *


@testClass
class SuiteTest(object):
	@test(suite="suite3")
	def atest():
		print "suite 3 test 1, in SuiteTest"
	
	@test(suite="suite1")
	def btest():
		print "suite 1 test 1, in SuiteTest"

@testClass
class SuiteTest2(object):
	@test(suite="suite1")
	def ctest():
		print "suite 1 test 2 in SuiteTest2"

@before
def before():
	print "before"

@after
def after():
	print "after"


@test(suite="suite1")
def test1():
	print "suite 1 test 1"

@test(suite="suite2")
def test2():
	print "suite 2 test 1"

@test
def test4():
	print "no suite test 1"

@test(suite="suite1")
def test3():
	print "suite 1 test 2"


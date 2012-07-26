from pyinq.tags import *

@test
def atest():
	print "main atest"

@testClass
class Class1(object):
	@test
	def atest():
		print "Class1 atest"
	
	@test
	def btest():
		print "Class2 btest"

@test
def btest():
	print "main test"

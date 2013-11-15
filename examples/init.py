from pyinq.asserts import *
from pyinq.tags import *

@testClass
class Class1:
	def __init__(self):
		self.num = 4

	@test
	def test1():
		assert_equal(self.num,4)
		self.num += 1
	
	@test
	def test2():
		assert_equal(self.num,4)
		self.num += 1

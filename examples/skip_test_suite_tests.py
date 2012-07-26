from pyinq.tags import *
from pyinq.asserts import *


@testClass(suite="suite2")
class Class1:
	@test
	def test3():
		assert_true(True)

	@skip
	@test(suite="suite1")
	def test1():
		assert_true(False)
	
	@test(suite="suite3")
	@skip
	def test2():
		assert_true(False)

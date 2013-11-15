from pyinq.tags import *
from pyinq.asserts import *
import mod

@test(expect=ValueError)
def test1():
	mod.parse("hjhwr")
	assert_true(True)

@test(expect=WindowsError)
def test2():
	mod.parse("hjhwr")

@test(expect=ValueError)
def test3():
	parse("4")

def parse(val):
	int(val)

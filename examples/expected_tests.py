from pyinq.tags import *
from pyinq.asserts import *
import mod

@test(expected=ValueError)
def test1():
	mod.parse("hjhwr")

@test(expected=WindowsError)
def test2():
	mod.parse("hjhwr")

@test(expected=ValueError)
def test3():
	parse("4")

def parse(val):
	int(val)

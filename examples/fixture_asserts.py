from pyinq.tags import *
from pyinq.asserts import *

@beforeClass
def setupClass():
	assert_true(False)

@before
def setup():
	assert_true(False)

@test
def test():
	print "TEST"
	assert_true(False)

@after
def teardown():
	assert_true("AFTER")

@afterClass
def teardownClass():
	assert_true(True)

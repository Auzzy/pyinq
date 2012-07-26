from pyinq.tags import *
from pyinq.asserts import *

@beforeSuite
@skip
def setup7():
	eval_true(False)

@skip
@beforeSuite
def setup8():
	eval_true(False)

@beforeModule
@skip
def setup5():
	eval_true(False)

@skip
@beforeModule
def setup6():
	eval_true(False)

@beforeClass
@skip
def setup3():
	eval_true(False)

@skip
@beforeClass
def setup4():
	eval_true(False)

@before
@skip
def setup1():
	eval_true(False)

@skip
@before
def setup2():
	eval_true(False)

@test
def test1():
	assert True

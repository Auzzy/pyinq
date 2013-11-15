from pyinq.asserts import *
from pyinq.tags import *

@test
def test1():
	eval_true(True)
	eval_true(False)
	eval_false(True)
	eval_false(False)
	eval_none(None)
	eval_none(8)
	eval_not_none(None)
	eval_not_none(8)
	eval_equal(4,4)
	eval_equal(4,5)
	eval_is(4,5)
	eval_is(4,4)
	eval_not_equal(4,4)
	eval_not_equal(4,5)
	eval_is_not(4,5)
	eval_is_not(4,4)
	eval_in(3,[1,1,2,3,5])
	eval_in(4,[1,1,2,3,5])
	eval_not_in(3,[1,1,2,3,5])
	eval_not_in(4,[1,1,2,3,5])
	eval_attrib(list,"append")
	eval_attrib(list(),"appends")
	eval_not_attrib(list,"appends")
	eval_not_attrib(list(),"append")


@test
def test2():
	assert_true(True)
	eval_true(False)
	eval_false(True)
	assert_false(False)
	assert_none(None)
	eval_none(8)
	eval_not_none(None)
	assert_not_none(8)
	assert_equal(4,4)
	assert_not_equal(4,5)
	eval_equal(4,5)

@test
def test3():
	assert_true(True)
	assert_true(False)
	eval_false(True)
	assert_false(False)
	assert_none(None)
	eval_none(8)
	eval_not_none(None)
	assert_not_none(8)
	assert_equal(4,4)
	eval_equal(4,5)

@test
def test4():
	assert_true(True)
	assert_none(raiseErr())
	assert_false(False)

@test
def test5():
	eval_true(True)
	eval_none(raiseErr())
	eval_false(False)

def raiseErr():
	raise IOError()

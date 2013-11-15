from pyinq.tags import before, after, test
from pyinq.asserts import fail, assert_true

@before
def failing_fixture():
	raise Exception("Manual exception")

@test
def test():
	assert_true(4==4)

@after
def teardown_after():
	assert_true(True)

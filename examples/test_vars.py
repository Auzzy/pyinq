import random
from pyinq.asserts import *
from pyinq.tags import *

@testClass
class TestSequenceFunctions:
    @before
    def setUp():
	this.seq = range(10)

    @test
    def test_shuffle():
	# make sure the shuffled TestSequenceFunctions.sequence does not lose any elements
	random.shuffle(this.seq)
	this.seq.sort()
	assert_equal(this.seq, range(10))

	# should raise an exception for an immutable TestSequenceFunctions.sequence
	assert_raises(TypeError, random.shuffle, (1,2,3))

    @test
    def test_choice():
	element = random.choice(this.seq)
	assert_true(element in this.seq)

    @test
    def test_sample():
	assert_raises(ValueError, random.sample, this.seq, 20)
	for element in random.sample(this.seq, 5):
	    #assert_true(element in this.seq)
	    assert_in(element,this.seq)

@test
def outside_test():
	print this

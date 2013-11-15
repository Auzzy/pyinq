import random
from pyinq.asserts import *
from pyinq.tags import *

@testClass
class TestSequenceFunctions:
    @before
    def setUp():
	self.seq = range(10)

    @test
    def test_shuffle():
	# make sure the shuffled TestSequenceFunctions.sequence does not lose any elements
	random.shuffle(self.seq)
	self.seq.sort()
	assert_equal(self.seq, range(10))

	# should raise an exception for an immutable TestSequenceFunctions.sequence
	assert_raises(TypeError, random.shuffle, (1,2,3))

    @test
    def test_choice():
	element = random.choice(self.seq)
	assert_true(element in self.seq)

    @test
    def test_sample():
	assert_raises(ValueError, random.sample, self.seq, 20)
	for element in random.sample(self.seq, 5):
	    #assert_true(element in self.seq)
	    assert_in(element,self.seq)

@test(expect=NameError)
def outside_test():
	print self

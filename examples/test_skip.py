from pyinq.tags import skip,test,before,testClass

@skip
@test
def test1():
    assert False

@test
@skip
def test2():
    assert False

@skip
@before
def fix1():
    assert False

@before
@skip
def fix2():
    assert False

@test
def fix3():
    assert False

@testClass
class Class1(object):
    @skip
    @test
    def clstest1():
        assert False

    @test
    @skip
    def clstest2():
        assert False
    
    @test
    def clstest3():
        assert False

skip(fix3)
skip(Class1.clstest3)

@skip
@testClass
class SkipClass1(object):
    @test
    def skip1test1():
        assert False
    
    @test
    def skip1test2():
        assert False

@testClass
@skip
class SkipClass2(object):
    @test
    def skip2test1():
        assert False
    
    @test
    def skip2test2():
        assert False

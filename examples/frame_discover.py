from pyinq.tags import *
from pyinq.asserts import *


@testClass
class Class1:
    @test(suite="frame")
    def test3():
        assert_true(True)

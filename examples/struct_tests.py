from pyinq.tags import *

@TestClass
class Class1(object):
	@BeforeClass
	def setupClass():
		print "setup Class1"
	
	@Before
	def setup():
		print "setup test in Class1"
	
	@Test
	def test1():
		print "test1 in Class1"
	
	@Test
	def test2():
		print "test2 in Class1"

	@After
	def tearDown():
		print "tear down test in Class1"
	
	@AfterClass
	def tearDownClass():
		print "tear down Class1"

@TestClass
class Class2(object):
	@BeforeClass
	def setupClass():
		print "setup Class2"
	
	@Before
	def setup():
		print "setup test in Class2"
	
	@Test
	def test1():
		print "test1 in Class2"
	
	@After
	def tearDown():
		print "tear down test in Class2"
	
	@AfterClass
	def tearDownClass():
		print "tear down Class2"

@BeforeModule
def setupModule():
	print "setup module"

@AfterModule
def tearDownModule():
	print "tear down module"

@BeforeClass
def setupMain():
	print "setup main"

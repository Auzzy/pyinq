from pyinq import discover_tests

if __name__=="__main__":
	suite = discover_tests('.')
	print "SUITE: " + str(suite.name)
	for module in suite:
		print "\tMODULE: " + str(module.name)
		for cls in module:
			print "\t\tCLASS: {cls.name} (SUITE: {cls.suite})".format(cls=cls)
			for test in cls:
				print "\t\t\tTEST: {test.name} (SUITE: {test.suite})".format(test=test)

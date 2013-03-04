from pyinq import discover_tests


if __name__=="__main__":
    suite = discover_tests('examples',"assert*")
    if suite:
        print "HERE"
        suite()

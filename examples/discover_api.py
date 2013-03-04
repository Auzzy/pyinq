from pyinq import discover_tests


if __name__=="__main__":
    print "EXAMPLES DISCOVER API TEST"
    suite = discover_tests('examples')
    if suite:
        suite()

tests = {}

# Exercise decorator, specifying that this function needs to be tested
def exercise(fun):
    tests[fun.__name__](fun)
    return fun

# Test decorator, specifying that this is a test for an exercise
def test(fun):
    tests[fun.__name__[5:]] = fun
    return fun
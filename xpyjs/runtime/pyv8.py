import glob
import sys
import os
import unittest
import PyV8

class Test(PyV8.JSClass, unittest.TestCase):

    AttributeError = AttributeError

    def __init__(self, methodName='puts'):
        PyV8.JSClass.__init__(self)
        unittest.TestCase.__init__(self, methodName)
        self.addTypeEqualityFunc(PyV8.JSArray, 'assertJSArrayEqual')

    def assertRaisesJSError(self, fun):
        self.assertRaises(PyV8.JSError, fun)

    def assertJSArrayEqual(self, expected, actual, msg=None):
        error = "%s != %s" % (expected, actual)

        if not isinstance(actual, PyV8.JSArray) or len(expected) != len(actual):
            raise self.failureException(error)

        for i in xrange(min(len(expected), len(actual))):
            if expected[i] != actual[i]:
                raise self.failureException('%s (first differing element %d: %s != %s' % (error, i, expected[i], actual[i]))

    def puts(self, txt):
        print txt

LIB_FILES = ['builtins.js', 'type.js', 'object.js', 'mro.js']
LIBS = '\n'.join([open(f).read() for f in LIB_FILES])
def makeContext(f):
    ctx = PyV8.JSContext(Test())
    ctx.enter()
    ctx.eval(LIBS)
    code = open(f).read()
    ctx.eval(code)
    return ctx

def makeMethod(path, methodName):
    def runit(self):
        ctx = makeContext(path)
        getattr(ctx.locals, methodName)()
    return runit

def makeTests(mod):
    path = 'tests/test-'+mod+'.js'

    ctx = makeContext(path)

    tests = {}
    for funName in dir(ctx.locals):
        if funName.find('test') == 0:
            tests[funName] = makeMethod(path, funName)

    testCase = type(mod,(Test,),tests)

    return map(testCase, tests.keys())

if __name__ == "__main__":


    suite = unittest.TestSuite()
    if len(sys.argv) == 2:
        suite.addTests(makeTests(sys.argv[1][:-3]))
    else:
        for t in glob.glob('tests/test-*.js'):
            suite.addTests(makeTests(os.path.basename(t)[5:-3]))

    unittest.TextTestRunner(verbosity=2).run(suite)


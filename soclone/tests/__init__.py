import doctest
import unittest

from soclone.tests import doctests
from soclone.tests import testcases

def suite():
    s = unittest.TestSuite()
    s.addTest(doctest.DocTestSuite(doctests))
    s.addTest(unittest.defaultTestLoader.loadTestsFromModule(testcases))
    return s

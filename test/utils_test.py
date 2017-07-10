u"""
test for utils function
"""
from seki import utils

import unittest

class SingletonTest(unittest.TestCase):
    def test_get_instance(self):
        @utils.singleton
        class Count():
            def __init__(self):
                self.i = 12


        count = Count()
        count.i = 33
        other_count = Count()

        self.assertEqual(count.i, other_count.i)

    def test_get_multi_instance(self):
        @utils.singleton
        class A():
            def __init__(self):
                self.i = 12

        @utils.singleton
        class B():
            def __init__(self):
                self.i = 14

        a = A()
        b = B()
        self.assertEqual(a.i, 12)
        self.assertEqual(b.i, 14)

if __name__ == "__main__":
    unittest.main()

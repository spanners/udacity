import unittest
from splay import *

# Licensed under the MIT license: 
# http://www.opensource.org/licenses/mit-license.php

class TestCase(unittest.TestCase):
    def setUp(self):
        self.keys = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.t = SplayTree()
        for key in self.keys:
            self.t.insert(key)

    def testInsert(self):
        for key in self.keys:
            self.assertEquals(key, self.t.find(key))

    def testRemove(self):
        for key in self.keys:
            self.t.remove(key)
            self.assertIsNone(self.t.find(key))

    def testLargeInserts(self):
        t = SplayTree()
        nums = 40000
        gap = 307
        i = gap
        while i != 0:
            t.insert(i)
            i = (i + gap) % nums

    def testIsEmpty(self):
        self.assertFalse(self.t.isEmpty())
        t = SplayTree()
        self.assertTrue(t.isEmpty())

    def testMinMax(self):
        self.assertEquals(self.t.findMin(), 0)
        self.assertEquals(self.t.findMax(), 9)
        t = SplayTree()
        self.assertIsNone(t.findMax())
        self.assertIsNone(t.findMin())

    def testInsertDuplicateKey(self):
        is_none = self.t.insert(1)
        self.assertIsNone(is_none)

    def testRemoveWhenNotInTree(self):
        with self.assertRaises(KeyNotFoundException) as ex:
            self.t.remove(-999)
        the_exception = ex.exception
        self.assertEquals(the_exception.value, -999)

    def testRemoveRootWhenLeftNotNone(self):
        temp_list = [1,9,2,8,3,7,4,6,5]
        t = SplayTree()
        for key in temp_list:
            t.insert(key)
        for key in temp_list:
            t.remove(key)
            self.assertEquals(t.find(key), None)


if __name__ == "__main__":
    unittest.main()

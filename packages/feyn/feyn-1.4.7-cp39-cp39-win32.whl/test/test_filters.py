import unittest

import numpy as np
from numpy.testing import assert_array_almost_equal

import feyn
import _feyn

class TestFilters(unittest.TestCase):

    def test_excludefunction(self):
        with self.subTest("Can use function name"):
            f = feyn.filters.ExcludeFunctions("gaussian")

            excluded = set(_feyn.get_specs()).difference(f.specs)
            self.assertEqual(excluded, {"cell:gaussian(i,i)->i", "cell:gaussian(i)->i"})


        with self.subTest("Can use function name list"):
            f = feyn.filters.ExcludeFunctions(["gaussian", "multiply"])

            excluded = set(_feyn.get_specs()).difference(f.specs)
            self.assertEqual(excluded, {"cell:gaussian(i,i)->i", "cell:gaussian(i)->i", "cell:multiply(i,i)->i"})


    def test_functions(self):
        with self.subTest("Can use function name"):
            f = feyn.filters.Functions("add")

            cellspecs = {s for s in f.specs if s.startswith("cell:")}
            self.assertEqual({"cell:add(i,i)->i"}, cellspecs)


        with self.subTest("Can use function name list"):
            f = feyn.filters.Functions(["add","multiply"])

            cellspecs = {s for s in f.specs if s.startswith("cell:")}
            self.assertEqual({"cell:add(i,i)->i", "cell:multiply(i,i)->i"}, cellspecs)

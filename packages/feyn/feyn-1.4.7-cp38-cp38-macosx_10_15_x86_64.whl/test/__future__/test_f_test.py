import unittest
from unittest.case import TestCase
import pytest

import numpy as np

from feyn.__future__.contrib.stats._stats_functions import _residual_square_sum, _f_statistic

class Test_Fstatistic(unittest.TestCase):

    def test_RSS(self):
        actuals = np.array([1,0.5,6])
        expected = 1
        sum = (0.5)**2 + 5**2
        assert(_residual_square_sum(actuals, expected) == sum)

    def test_f_statistic(self):
        rss_restricted = 25
        rss_mini = 10
        no_samples = 10
        no_parameters = 4
        no_hypoth_para = 1
        act = (15 * (10 - 4)) / 10
        F, _ = _f_statistic(rss_restricted, rss_mini, no_samples, no_parameters, no_hypoth_para)
        assert(F == act)
import unittest
import pytest
import matplotlib.pyplot as plt

import numpy as np

from feyn.plots._probability_plot import _pos_neg_classes
from feyn.plots._probability_plot import plot_probability_scores

class TestProbPlot(unittest.TestCase):

    def setUp(self):
        self.true = np.array([0,1,1,0])
        self.pred = np.array([0.9, 0.3, 0.8, 0])

    def test_pos_neg_classes(self):
        x, y =_pos_neg_classes(self.true, self.pred)
        assert(x == np.array([0.8,0.3])).all()
        assert(y == np.array([0,0.9])).all()

    def test_prob_scores(self):
        ax = plot_probability_scores(self.true, self.pred)

        assert(ax is not None)

    def test_axis(self):
        _, ax = plt.subplots()
        ax = plot_probability_scores(self.true, self.pred, ax=ax)
        assert(ax is not None)

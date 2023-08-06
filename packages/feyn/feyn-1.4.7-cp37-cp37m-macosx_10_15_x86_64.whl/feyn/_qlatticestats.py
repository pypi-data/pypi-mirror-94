"""Module for LatticeStateStats class."""
from typing import Dict

import numpy as np

import feyn

class LatticeStateStats:
    """Object that manages data for many statistics measured in the QLattice simulator."""

    def __init__(self, stats_dict:Dict) -> "LatticeStateStats":
        """
        Arguments:
            stats_dict {Dict} -- The dictionary that lives in Simulator._stats_dict in the QLattice.

        Returns:
            LatticeStateStats -- Handy object that you can query for the generation of graph probabilities.
        """
        from pandas import DataFrame
        self._dat = DataFrame.from_dict(stats_dict)
        self._nparticles = len(self._dat)

    def __repr__(self) -> str:
        return "Tracking {} for {} particles.".format(
            list(self._dat.columns),
            self._nparticles
        )

    def dat_df(self) -> "DataFrame":
        """Return the Pandas DataFrame of statistics tracked."""
        return self._dat

    def query_graph_prob(self, graph:feyn.Graph) -> float:
        """Query this lattice with a graph configuration to find the probability of it generating a graph like specified in the qconf.

        Arguments:
            qconf {Dict[str, int]} -- The query as a graph configuration. Maps the statistics we track to their value.

        Raises:
            ValueError: Query configuration contains references to statistics not tracked.

        Returns:
            float -- The probability of the lattice generating a graph like specified in the qconf.
        """
        qconf = self._graph_to_query(graph)
        return self.query_prob(qconf)

    def query_prob(self, qconf:Dict[str, int]) -> float:
        """Query this lattice with a graph configuration to find the probability of it generating a graph like specified in the qconf.

        Arguments:
            qconf {Dict[str, int]} -- The query as a graph configuration. Maps the statistics we track to their value.

        Raises:
            ValueError: Query configuration contains references to statistics not tracked.

        Returns:
            float -- The probability of the lattice generating a graph like specified in the qconf.
        """
        if not set(qconf.keys()).issubset(self._dat.columns):
            raise ValueError("Query configuration contains references to statistics not tracked.")

        bool_idx = np.full((len(self._dat),), True)
        for stat, val in qconf.items():
            stat_idx = self._dat[stat] == val
            bool_idx = bool_idx & stat_idx

        return bool_idx.sum() / self._nparticles

    def _graph_to_query(self, graph:feyn.Graph) -> Dict[str, int]:
        """Take a graph from feyn and turn it into a query to ask a LatticeStateStats object how likely we are to generate a graph like this.

        Arguments:
            graph {feyn.Graph} -- The graph you want to turn into a query.

        Returns:
            Dict[str, int] -- Your query, the configuration of the input graph described by various statistics.
        """
        ret = {
            "depth": graph.depth,
            "n_edges": graph.edge_count,
            "n_unary": 0,
            "n_binary": 0,
            "n_events": 0
        }
        for interaction in graph:
            ret["n_events"] += 1
            if interaction.spec.startswith("in") or interaction.spec.startswith("out"):
                continue
            if len(interaction.sources) == 2:
                ret["n_binary"] += 1
            else:
                ret["n_unary"] += 1
        return ret

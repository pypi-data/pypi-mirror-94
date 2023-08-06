import numpy as np
from typing import Union, List
from feyn import Graph


def _set_node_strength(graph: Graph,
                       nodes: Union[str, int, List[int]]="all",
                       strength: Union[float, List[float]]=1.0):
    """Set the strength of a single node or a list of nodes
    of the given graph.

    Arguments:
        graph {Graph} -- graph whose node strengths will be changed

    Keyword Arguments:
        nodes {Union[str, int, List[int]]} -- nodes whose strengths will be changed (default: "all")
        strength {Union[float, List[float]]} -- new strength values to be given to
        the specified nodes (default: 1.0)

    Returns:
        Graph -- copy of input graph with new node strengths
    """

    graph_copy = Graph._from_dict(graph._to_dict().copy())

    if hasattr(nodes, "__len__"):
        if nodes == "all":
            nodes = np.arange(len(graph_copy))
        elif all(isinstance(elem, (np.int, np.int64)) for elem in nodes):
            if len(nodes) > len(graph_copy):
                raise ValueError("Array of nodes has size bigger than the actual number of interactions in the given graph!")
            pass
        else:
            raise TypeError("Parameter nodes must be 'all', an integer or a list of integers.")

        if not hasattr(strength, "__len__"):
            strength = strength * np.ones_like(nodes)
        elif len(strength) != len(nodes):
            raise ValueError("Length of strength array must be the same as nodes array!")

        for i, n in enumerate(nodes):
            graph_copy[n]._strength = strength[i]

    elif not hasattr(nodes, "__len__") and not hasattr(strength, "__len__"):
        graph_copy[nodes]._strength = strength

    else:
        raise TypeError("The types of nodes and strength parameters are incompatible. If nodes is type int, then strength shouldn't be a list!")

    return graph_copy

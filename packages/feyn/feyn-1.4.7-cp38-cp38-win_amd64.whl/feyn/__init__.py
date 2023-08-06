"""Feyn is the main Python module to build and execute models that utilizes a QLattice.

The QLattice stores and updates probabilistic information about the mathematical relationships (models) between observable quantities.

The workflow is typically:

# Connect to the QLattice
>>> ql = feyn.QLattice()

# Extract a Regression QGraph
>>> qgraph = gl.get_regressor(data.columns, output="out")

# Fit the QGraph to a local dataset
>>> qgraph.fit(data)

# Pick the best Graph from the QGraph
>>> graph = qgraph[0]

# Possibly update the QLattice with the graph to make the QLattice better at this kind of model in the future
>>> ql.update(graph)

# Or use the graph to make predictions
>>> predicted_y = graph.predict(new_data)
"""
from ._version import read_version, read_git_sha
from _feyn import Interaction
from ._svgrenderer import SVGRenderer
from ._graph import Graph
from ._sgdtrainer import SGDTrainer
from ._qgraph import QGraph

from ._snapshots import SnapshotCollection, Snapshot
from ._qlattice import QLattice
from ._register import Register

from ._config_evolution_params import _HalfLife_params

from . import tools
from . import losses
from . import filters
from . import metrics
from . import plots
from . import reference

_current_renderer = SVGRenderer

__all__ = ['QLattice', 'QGraph', 'Graph', 'Interaction', 'SnapshotCollection', 'Snapshot']

__version__ = read_version()
__git_sha__ = read_git_sha()

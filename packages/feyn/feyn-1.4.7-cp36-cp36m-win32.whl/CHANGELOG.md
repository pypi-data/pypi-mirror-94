# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

New changes goes here..

## [1.4.7] - 2021-02-12

### Changed

- General performance improvements in finding good graphs.

### Added

- Add roc_auc_score to `feyn.metrics` which will calculate the AUC of a graph. (Also accessible on `graph.roc_auc_score`).
- Plotting style improvements:
  - 'light' is now usable as alias to 'default' when setting theme.
  - Matplotlib plot styling now matches the theme choice.
  - Added colormaps to use with matplotlib: 'feyn', 'feyn-diverging'. 'feyn-partial', 'feyn-primary', 'feyn-secondary', 'feyn-highlight', 'feyn-accent'.
- Added `FeatureImportanceTable` to `feyn.insights`. (The equivalent functionality was previous in `pdheatmap` from `__future__`).
- (__future__) Add various stats functions. `graph_f_score` and `plot_graph_p_value`.

## [1.4.6] - 2021-01-08

### Added

- Targeted Maximum Likelihood Estimation (TMLE) introduced in `feyn.inference`. [See more in our docs](https://docs.abzu.ai/docs/guides/advanced/tmle.html)

### Changed

- Default graphs sort back to loss_value instead of bic.
- `feyn.tools.simpify_graph` default option is now to not formulate the logistic function, but instead output “logreg(…)“. Use argument `symbolic_lr=True` if you want to keep previous behavior.
- Categorical variables rendered in the sympify function from category(<X_featurename>) to category_<featurename>.

## [1.4.5] - 2020-12-18

### Added

- Python 3.9 support

### Fixed

- Fix memory bug when handling many registers (>165) in QLattice.

## [1.4.4] - 2020-12-18

### Removed

- `metrics.get_mutual_information()`, `metrics.get_pearson_correlations()`, `metrics.get_summary_information()`. The functionality is now covered by `metrics.calculate_mi()`, `metrics.calculate_pc()` in the public API.

### Changed

- Even more general performance improvements.

## [1.4.3] - 2020-12-04

### Changed

- General performance improvements.

### Added

- `Graph.plot_partial()` and `Graph.plot_partial2d()` to analyze the graph response.
- `metrics.calculate_mi()`, `metrics.calculate_pc()` to calculate mutual information and pearson correlations.

## [1.4.2] - 2020-10-26

- `Graph.sympify()` which returns a sympy expression mathcing the graph
- Mutual information and pearson correlations are now calculated on entire data set, giving more accurate results
- `Graph.fit()` function which can be used to fit or refit a single graph on a dataset
- Adding support to both numerical and categorical partial dependence plots
- Bugfix: 1d plots with categoricals ordered wrt their weights
- Bugfix: Fix support np-dict for graph_summary

## [1.4.1] - 2020-10-09

- Added linear and constant reference models (in `feyn.reference`) to compare with and calculate p-values (lives in `feyn.metrics`).
- Graph vizualizations rewritten and much improved.
- Dark theme support!

## [1.4.0] - 2020-09-03

- ql.update now accepts either a single graph or a list of graphs.
- Added methods: `QLattice.get_regressor` and `QLattice.get_classifier` to replace  `QLattice.get_qgraph`.
- New mathematical functions: `add`, `exp` and `log`.
- You can now control functions in graphs with new filters: `feyn.filters.Functions(["add", "multiply"])` and `feyn.filters.ExcludeFunctions("sine")`.
- New plot. ROC-curves.

## [1.3.3] - 2020-08-14

- Shorthands for plotting and score utility functions on feyn.Graph
- New approach to damping learning rates lead to more accurate fits
- Max-depth filter is less strict on which type of integers it accepts.
- Add automatric retries on failed http-requests
- Configurations can now also be stored in `<home_folder>/.config/.feynrc`

## [1.3.1] - 2020-07-07

- The new automatic scalar is now default on both input and output.
- Alternative input and output semantic types (f#) that does not scaling

## [1.3.0] - 2020-07-06

- Added a new scaler: f$. It is more automatic.

## [1.2.1] - 2020-06-16

- Changed the configuration environment variable `QLATTICE_BASE_URI` to `FEYN_QLATTICE_URL`.
- Changed the configuration environment variable `FEYN_TOKEN` to `FEYN_QLATTICE_API_TOKEN`.
- Support for configuration via config file. `feyn.ini` or `.feynrc` located in your home folder.
- Breaks compatibility with qlattice <= 1.1.2
  - Removed the neeed to add registers via qlattice.registers.get (and removed qlattice.registers.get)
  - New parameter to get_qgraph function to choose the semantic type of the data colums (this replaces the need cat/fixed register types)
- Fixes bug with numpy 1.15 and multiarray import in windows 64bit

## [1.1.2] - 2020-05-11

- Added Windows Support!
- Removed dependency to GraphViz
- Removed dependency to scikit-learn

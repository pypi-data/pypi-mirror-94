Python bindings to https://github.com/aforren1/psydapt.

For now, see the C++ documentation for details: https://aforren1.github.io/psydapt/index.html

See the demos/ folder for examples.

Wheels are not yet on PyPI, but can be found under "Artifacts" in the latest successful workflow run here: https://github.com/aforren1/psydapt-py/actions

```python
from psydapt import Scale
import psydapt.questplus as qp
from psydapt.staircase import Staircase
from psydapt.questplus import Weibull

x = Staircase(Staircase.Params(
    start_val=0.5,
    n_reversals=3,
    step_sizes=[0.01, 0.001],
    n_trials=20,
    n_up=4,
    n_down=3,
    apply_initial_rule=True,
    stim_scale=Scale.Linear,
    min_val=0
))

intensities = [-3.5, -3.25, -3, -2.75, -2.5,
               -2.25, -2, -1.75, -1.5, -1.25,
               -1, -0.75, -0.5]
y = Weibull(Weibull.Params(
    stim_scale=Scale.Log10,
    intensity=intensities,
    threshold=intensities,
    slope=[0.5, 4.125, 7.75, 11.375, 15],
    lower_asymptote=[0.01, 0.1325, 0.255, 0.3775, 0.5],
    lapse_rate=[0.01],
    stim_selection_method=qp.StimSelectionMethod.MinEntropy, # only MinEntropy for now
    param_estimation_method=qp.ParamEstimationMethod.Mean, # currently unused
    n=5, # currently unused
    max_consecutive_reps=2, # currently unused
    random_seed=1 # currently unused
))


```

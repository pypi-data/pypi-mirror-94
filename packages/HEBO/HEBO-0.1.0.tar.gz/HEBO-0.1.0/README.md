![](hebo.png)

*Note from uploader: This is a fork of the original [project](https://github.com/huawei-noah/noah-research/tree/master/HEBO) with several minor modifications. I have uploaded this package to PyPi in accordance with the MIT License for distribution purposes and do not claim ownership of any work not done by me. I will happily give up control of the package to the original authors should they wish so.* 

# README

Bayesian optimsation library developped by Huawei Noahs Ark Decision Making and Reasoning (DMnR) lab. The <strong> winning submission </strong> to the [NeurIPS 2020 Black-Box Optimisation Challenge](https://bbochallenge.com/leaderboard). 

Summary             |  Ablation
:-------------------------:|:-------------------------:
[Results]( https://github.com/huawei-noah/noah-research/blob/master/HEBO/summary_plot2.pdf) | [Results](https://github.com/huawei-noah/noah-research/blob/master/HEBO/summary_ablation2.pdf)

# Contributors 

<strong> Alexander I. Cowen-Rivers, Wenlong Lyu, Zhi Wang, Antoine Grosnit, Rasul Tutunov, Hao Jianye, Jun Wang, Haitham Bou Ammar. </strong>

## Installation

```bash
python setup.py develop
```

## Demo

```python
import pandas as pd
import numpy  as np
from hebo.design_space.design_space import DesignSpace
from hebo.optimizers.hebo import HEBO

def obj(params : pd.DataFrame) -> np.ndarray:
    return ((params.values - 0.37)**2).sum(axis = 1).reshape(-1, 1)
        
space = DesignSpace().parse([{'name' : 'x', 'type' : 'num', 'lb' : -3, 'ub' : 3}])
opt   = HEBO(space)
for i in range(5):
    rec = opt.suggest(n_suggestions = 4)
    opt.observe(rec, obj(rec))
    print('After %d iterations, best obj is %.2f' % (i, opt.y.min()))
```

## Auto Tuning via Sklearn Estimator

```python
from sklearn.datasets import load_boston
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error

from hebo.sklearn_tuner import sklearn_tuner

space_cfg = [
    {'name' : 'max_depth', 'type' : 'int', 'lb' : 1, 'ub' : 20},
    {'name' : 'min_samples_leaf', 'type' : 'num', 'lb' : 1e-4, 'ub' : 0.5},
    {'name' : 'max_features', 'type' : 'cat', 'categories' : ['auto', 'sqrt', 'log2']},
    {'name' : 'bootstrap', 'type' : 'bool'},
    {'name' : 'min_impurity_decrease', 'type' : 'pow', 'lb' : 1e-4, 'ub' : 1.0},
    ]
X, y   = load_boston(return_X_y = True)
result = sklearn_tuner(RandomForestRegressor, space_cfg, X, y, metric = r2_score, max_iter = 16)
```

## Documentation

```bash
cd doc
make html
```

You can view the compiled documentation in `doc/build/html/index.html`.

## Test

```bash
pytest -v test/ --cov ./hebo --cov-report term-missing --cov-config ./test/.coveragerc
```

## Reproduce Experimental Results

- See `archived_submissions/hebo`, which is the exact submission that won the NeurIPS2020 Black-Box Optimsation Challenge.
- Use `run_local.sh` in [bbo_challenge_starter_kit](https://github.com/rdturnermtl/bbo_challenge_starter_kit/) to reproduce `bayesmark` experiments, you can just drop `archived_submissions/hebo` to the `example_submissions` directory.
- The `MACEBO` in `hebo.optimizers.mace` is the same optimiser, with same hyperparameters but a modified interface (bayesmark dependency removed).


## Features

- Continuous, integer and categorical design parameters.
- Constrained and multi-objective optimsation.
- Contextual optimsation.
- Multiple surrogate models including GP, RF and BNN.
- Modular and flexible Bayesian Optimisation building blocks.


## Cite Us

Cowen-Rivers, Alexander I., et al. "HEBO: Heteroscedastic Evolutionary Bayesian Optimisation." arXiv preprint arXiv:2012.03826 (2020).

## BibTex

@article{cowen2020hebo,
  title={HEBO: Heteroscedastic Evolutionary Bayesian Optimisation},
  author={Cowen-Rivers, Alexander I and Lyu, Wenlong and Wang, Zhi and Tutunov, Rasul and Jianye, Hao and Wang, Jun and Ammar, Haitham Bou},
  journal={arXiv preprint arXiv:2012.03826},
  year={2020}
}

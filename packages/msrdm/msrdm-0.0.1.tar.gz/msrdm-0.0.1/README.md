# Multi-Stage Robust Decision Making (MSRDM)
Multi-Stage Robust Decision Making (MSRDM) is a decision-support framework under deep uncertainty.

## Installation
MSRDM runs on Python 3.8 or higher.

Dependencies are numpy and pandas. Optional dependencies are matplotlib, seaborn, and plotly, which are required for plotting functions.

It can be installed by

```sh
pip install msrdm
```

## Usage

### HoU Analysis

```python
from msrdm.uncertainty import RealUncertainParameter, EllipticUncertaintyRegion

# Define uncertain parameters
w1 = RealUncertainParameter('w1', nominal=0, lower_deviation=1, upper_deviation=1, dog='greater')
w2 = RealUncertainParameter('w2', nominal=3, lower_deviation=4, upper_deviation=5, dog='greater')

# Define uncertain region
uncertainty_region = EllipticUncertaintyRegion([w1, w2])

# Define objective function
def func(x, w):

```

## License

- [BSD 3-Clause License](https://choosealicense.com/licenses/bsd-3-clause/)

from pathlib import Path
import numpy as np
import pandas as pd
import plotly.express as px

from assignment_4.monte_carlo.model import do_monte_carlo
from assignment_4.config import BLD, SRC

pd.options.mode.copy_on_write = True
pd.options.future.infer_string = True
pd.options.plotting.backend = "plotly"


def task_run_monte_carlo_simulation(produces: Path = BLD / "python" / "models" / "monte_carlo_results.pkl"):
    "Run Monte Carlo simulation with given values of arguments."
    true_params = np.ones(6)
    y_sd = 1.5
    cov_type = "random"
    mean = np.zeros(len(true_params))
    meas_sds = np.linspace(0, 5, 10) # measurement error std
    n_repetitions = 200
    seed = 925408
    n_obs = 2_000

    data = do_monte_carlo(true_params, y_sd, cov_type, mean, meas_sds, n_repetitions,seed, n_obs)

    data.to_pickle(produces)

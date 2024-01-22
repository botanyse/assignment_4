"""Tasks running the results formatting (tables, figures)."""

from pathlib import Path

import pandas as pd
import pytask

pd.options.mode.copy_on_write = True
pd.options.future.infer_string = False
pd.options.plotting.backend = "plotly"

from assignment_4.config import BLD, SCORE_NAMES
from assignment_4.final.plot import create_plots, plot_monte_carlo

dep = {
    "scripts": Path("plot.py"),
    "data": BLD / "python" / "data" / "merged_chs_nlsy_data.csv",
}

for seed, id_ in SCORE_NAMES.items():

    @pytask.task(id=id_)
    def task_create_plots(
        depends_on=dep,
        produces=BLD / "python" / "figures" / f"plot_{seed}.png",
        seed=seed,
        id_=id_,
    ):
        """Create plots of the score for every attribute calculated against the scores
        in the chs dataset by age group and write them in html files.
        """
        merged_data = pd.read_csv(depends_on["data"])
        fig = create_plots(merged_data, x=seed, y=id_)
        fig.write_image(produces, width=1080, height=720)


def task_plot_monte_carlo_simulation(
    path_to_data: Path = BLD / "python" / "models" / "monte_carlo_results.pkl",
    produces: Path = BLD / "python" / "figures" / "monte_carlo_bias.png",
):
    data = pd.read_pickle(path_to_data)
    fig = plot_monte_carlo(data)
    fig.write_image(produces, width=1080, height=720)

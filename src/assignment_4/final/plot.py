"""Functions plotting results."""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

pd.options.mode.copy_on_write = True
pd.options.future.infer_string = True
pd.options.plotting.backend = "plotly"


def create_plots(df, x,  y):
    """Create plots of the score for every attribute calculated against the scores in the chs dataset by age group and write them in html files
    """
    fig = px.scatter(df, x, y, facet_col="age", trendline="ols")
    return go.Figure(fig)


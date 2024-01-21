"""Functions plotting results."""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

pd.options.mode.copy_on_write = True
pd.options.future.infer_string = True
pd.options.plotting.backend = "plotly"


def create_plots(df, x,  y):
    """Creates a scatter plot with a trendline for each age group.

    This function uses Plotly Express to create a scatter plot. The x and y axes represent the scores 
    for two attributes. The plot is faceted by the 'age' column, meaning there is a separate plot for 
    each age group. A trendline is also added to each plot using the method of ordinary least squares (OLS).

    Args:
        df (pandas.DataFrame): The dataframe containing the data to plot. It should have columns 
        corresponding to the x and y parameters, as well as an 'age' column.
        x (str): The name of the column in df to use as the x values.
        y (str): The name of the column in df to use as the y values.

    Returns:
        plotly.graph_objects.Figure: The figure object representing the plot.

    """
    fig = px.scatter(df, x=x, y=y, facet_col="age", trendline="ols")
    return go.Figure(fig)
    

def plot_monte_carlo(data):
    """
    Plots the bias as a function of measurement standard deviation for each independent variable.

    This function uses Plotly Express to create a line plot. The x-axis represents the measurement 
    standard deviation ('meas_sd'), the y-axis represents the bias, and different independent variables are 
    distinguished by color.

    Args:
        data (pandas.DataFrame): The dataframe containing the data to plot. It should have columns 
        'bias', 'meas_sd', and 'name' where 'name' represents each independent variable.

    Returns:
        plotly.graph_objects.Figure: The figure object representing the plot.

    """
    fig = px.line(
        data_frame=data,
        y="bias",
        x="meas_sd",
        color="name",
    )
    return fig
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

pd.options.mode.copy_on_write = True
pd.options.future.infer_string = True
pd.options.plotting.backend = "plotly"


def do_monte_carlo(
    true_params,
    y_sd,
    cov_type,
    mean,
    meas_sds,
    n_repetitions,
    seed,
    n_obs,
):
    """Run a Monte Carlo simulation for a multivariate linear regression to study the
    impact of measurement error in the first independent variable.

    Args:
        true_params (numpy.ndarray): The true coefficients vector of regression model
        y_sd (float): The standard deviation of the error term, i.e. of dependent variable y
        cov_type (str): The type of covariance-matrix of independent variables,
        either "random" or "deterministic"
        mean (numpy.ndarray): The expected values of independent variables
        meas_sds (numpy.ndarray): The standard deviation of measurement errors
        n_repetitions (int): Number of repetitions in the simulation
        seed (int): A random number generator seed
        n_obs (int): Number of observations

    Returns:
        data (DataFrame): Simulation result of Bias, Root-Mean-Square Deviation (rmse), and Standard Deviation of Measurement Error(meas_sd) for each independent x variable.

    Raises:
        ValueError: If invalid cov_type input is given.

    """
    _fail_if_parameters_not_numerical(true_params)
    _fail_if_meas_sds_negative(meas_sds)
    _fail_if_y_sd_negative(y_sd)
    _fail_if_seed_not_hashable(seed)
    _fail_if_cov_type_not_valid(cov_type)
    _fail_if_n_non_positive(n_obs)
    _fail_if_n_non_positive(n_repetitions)
    _fail_if_mean_string(mean)

    rng = np.random.default_rng(seed)
    n_params = len(true_params)
    # Set up parameter names for plotting
    names = [f"x_{i}" for i in range(len(true_params))]
    # Initialize list to which we will append DataFrames that are concatenated later
    to_concat = []
    for meas_sd in meas_sds:
        cov = _generate_cov_matrix(cov_type, n_params, rng)
        # Set up a list to which we will append parameter estimates
        estimates = []
        for _ in range(n_repetitions):
            x, y, _ = _generate_independent_and_dependent_variables(
                mean,
                cov,
                n_obs,
                y_sd,
                rng,
                true_params,
            )
            x = _generate_measurement_error(x, meas_sd, n_obs, rng)
            params = LinearRegression().fit(x, y).coef_
            # append them to the list of estimates
            estimates.append(params)

        # Set up empty DataFrame and add results we need for plotting

        df = pd.DataFrame()
        deviations = np.array(estimates) - true_params
        df["name"] = names
        df["bias"] = deviations.mean(axis=0)
        df["rmse"] = np.sqrt((deviations**2).mean(axis=0))
        df["meas_sd"] = meas_sd
        to_concat.append(df)

    # Concatenate the DataFrame
    return pd.concat(to_concat)


def _generate_cov_matrix(cov_type, n_params, rng):
    """Generate a random or deterministic variance-covariance matrix.

    Args:
        cov_type (str): Type of covariance matrix to generate. Must be 'random' or 'deterministic'.
        n_params (int): Number of parameters. This determines the dimensions of the covariance matrix.
        rng (numpy.random.Generator): Random number generator.

    Returns:
        numpy.ndarray: The generated variance-covariance matrix. It is a symmetric positive semi-definite matrix.

    Raises:
        ValueError: If `cov_type` is not 'random' or 'deterministic'.

    """
    if cov_type == "deterministic":
        cov = np.eye(n_params) + 0.2
    elif cov_type == "random":
        # Create a random but valid (i.e. symmetric positive semi-definite)
        # covariance matrix by multiplying a random matrix with its transpose
        # every matrix UU.T is positive semidefinite
        # and adding 1 to the diagonal to improve conditioning
        # because adding 1 to the diagonal ensures that our matrix is
        # always invertible
        helper = rng.uniform(low=-1, high=1, size=(n_params, n_params))
        cov = helper @ helper.T + np.eye(n_params)

    return cov


def _generate_independent_and_dependent_variables(
    mean,
    cov,
    n_obs,
    y_sd,
    rng,
    true_params,
):
    """Generate independent and dependent variables for a multivariate normal
    distribution.

    Args:
        mean (numpy.ndarray): Mean values for the multivariate normal distribution.
        cov (numpy.ndarray): Covariance matrix for the multivariate normal distribution.
        n_obs (int): Number of observations to generate.
        y_sd (float): Standard deviation of the error term in the dependent variable.
        rng (numpy.random.Generator): Random number generator.
        true_params (numpy.ndarray): True parameters for the linear model.

    Returns:
        tuple: A tuple containing:
            - x (numpy.ndarray): Independent variables.
            - y (numpy.ndarray): Dependent variable.
            - epsilon (numpy.ndarray): Error term added to the dependent variable.

    """
    x = rng.multivariate_normal(mean=mean, cov=cov, size=n_obs)
    # Draw error
    epsilon = rng.normal(loc=0, scale=y_sd, size=n_obs)
    # Calculate y (before adding measurement error!)
    y = x @ true_params + epsilon

    return x, y, epsilon


def _generate_measurement_error(x, meas_sd, n_obs, rng):
    """Generate measurement error and add it to the independent variables.

    Args:
        x (numpy.ndarray): Independent variables.
        meas_sd (float): Standard deviation of the measurement error.
        n_obs (int): Number of observations.
        rng (numpy.random.Generator): Random number generator.

    Returns:
        numpy.ndarray: Independent variables with added measurement error.

    Notes:
        The measurement error is added to the first column of the independent variables `x`.

    """
    meas_error = rng.normal(loc=0, scale=meas_sd, size=n_obs)
    # Add measurement error
    x[:, 0] += meas_error
    return x


def _fail_if_parameters_not_numerical(sr):
    if np.any([isinstance(i, str) for i in sr]):
        report = "Parameter cannot be a string."
        raise TypeError(report)


def _fail_if_meas_sds_negative(sr):
    if np.any(sr < 0):
        report = "Standard deviation of measurement error cannot be negative."
        raise ValueError(report)


def _fail_if_y_sd_negative(sr):
    if sr < 0:
        report = "Standard deviation of dependent variable y cannot be negative."
        raise ValueError(report)


def _fail_if_seed_not_hashable(seed):
    try:
        hash(seed)
    except TypeError:
        raise


def _fail_if_cov_type_not_valid(str):
    if not (str == "deterministic" or str == "random"):
        report = f"Invalid cov_type: {str}. Must be 'random' or 'deterministic'"
        raise ValueError(
            report,
        )


def _fail_if_n_non_positive(obs):
    if obs <= 0:
        report = f"Invalid number of observations: {obs}. Must be a positive integer."
        raise ValueError(report)


def _fail_if_mean_string(param):
    if isinstance(param, str):
        msg = "Mean cannot be a string."
        raise TypeError(msg)

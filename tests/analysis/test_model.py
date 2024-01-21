import numpy as np
import pandas as pd
import pytest
from sklearn.linear_model import LinearRegression
from scipy import stats
from assignment_4.monte_carlo.model import do_monte_carlo, _generate_cov_matrix, _generate_independent_and_dependent_variables, _generate_measurement_error

pd.options.mode.copy_on_write = True
pd.options.future.infer_string = True
pd.options.plotting.backend = "plotly"

@pytest.fixture
def inputs():
    return {
    "true_params" : np.ones(6),
    "y_sd" : 1.5,
    "cov_type" : "random",
    "mean" : np.zeros(6),
    "meas_sds" : np.linspace(0, 5, 10),
    "n_repetitions" : 200,
    "seed" : 925408,
    "n_obs" : 2_000,
    }


def test_do_monte_carlo_x0_parameter_biased_towards_zero(inputs):
    data = do_monte_carlo(**inputs)
    x = data.loc[data["name"] == "x_0", ["bias"]]
    x = x.iloc[3:] # taking bias values where it converges to -1
    actual =x.reset_index(drop=True).values
    expected = -np.ones_like(actual)
    np.testing.assert_array_almost_equal(np.round(actual),np.round(expected))

# alternative way of checking attenuation bias

def test_x0_parameter_bias_significance(inputs):
    data = do_monte_carlo(**inputs)
    parameter_estimates = data[data['name'] == 'x_0']['bias'].values

    # Perform a one-sample t-test against the null hypothesis of zero bias
    t_stat, p_value = stats.ttest_1samp(parameter_estimates, 0)

    assert p_value < 0.05 


def test_generate_cov_matrix_is_positive_semi_definite(inputs):
    rng = np.random.default_rng(inputs["seed"])
    cov = _generate_cov_matrix(inputs["cov_type"],len(inputs["true_params"]),rng)
    assert np.all(np.linalg.eigvals(cov) >= 0)


def test_generate_independent_and_dependent_variables_correct_shape(inputs):
    rng = np.random.default_rng(inputs["seed"])
    mean, cov_type, n_obs, y_sd, true_params= inputs["mean"], inputs["cov_type"], inputs["n_obs"], inputs["y_sd"], inputs["true_params"]
    n_params = len(true_params)
    cov = _generate_cov_matrix(cov_type, n_params, rng)
    X, y, epsilon = _generate_independent_and_dependent_variables(
                mean, cov, n_obs, y_sd, rng, true_params)

    # test if X and y have the correct shape
    assert X.shape == (n_obs, n_params)
    assert y.shape == (n_obs,)

    expected_y = X @ true_params + epsilon

    np.testing.assert_array_almost_equal(y, expected_y, decimal=1)


def test_generate_measurement_error_changed_x0_value(inputs):
    rng = np.random.default_rng(inputs["seed"])
    n_obs, n_params = inputs["n_obs"], len(inputs["true_params"])
    x = rng.normal(size=(n_obs,n_params))
    x_c = x.copy()
    meas_sd = 2.0

    x_with_error = _generate_measurement_error(x, meas_sd, n_obs,rng)

    assert np.all(x_with_error[:, 1:] == x_c[:, 1:])

    assert not np.array_equal(x_with_error[:, 0], x_c[:, 0])


def test_input_negative_std_deviation_of_meas_error(inputs):
    true_params = inputs["true_params"]
    y_sd  = inputs["y_sd"]
    cov_type = inputs["cov_type"],
    mean = inputs["mean"]
    meas_sds = np.array([-2, 3])
    n_repetitions = inputs["n_repetitions"]
    seed = inputs["seed"]
    n_obs = inputs["n_obs"]

    with pytest.raises(ValueError) as excinfo:
        do_monte_carlo(true_params, y_sd, cov_type, mean, meas_sds, n_repetitions,seed, n_obs)

    assert "Standard deviation of measurement error cannot be negative." == str(excinfo.value)


def test_input_negative_y_std(inputs):
    true_params = inputs["true_params"]
    y_sd  = -inputs["y_sd"]
    cov_type = inputs["cov_type"]
    mean = inputs["mean"]
    meas_sds = inputs["meas_sds"]
    n_repetitions = inputs["n_repetitions"]
    seed = inputs["seed"]
    n_obs = inputs["n_obs"]

    with pytest.raises(ValueError) as excinfo:
        do_monte_carlo(true_params, y_sd, cov_type, mean, meas_sds, n_repetitions,seed, n_obs)

    assert "Standard deviation of dependent variable y cannot be negative." in str(excinfo.value)



def test_input_string_parameter_vector(inputs):
    true_params = np.array([1,1,1,"string",1,1])
    y_sd  = inputs["y_sd"]
    cov_type = inputs["cov_type"]
    mean = inputs["mean"]
    meas_sds = inputs["meas_sds"]
    n_repetitions = inputs["n_repetitions"]
    seed = inputs["seed"]
    n_obs = inputs["n_obs"]
    
    with pytest.raises(TypeError) as excinfo:
        do_monte_carlo(true_params, y_sd, cov_type, mean, meas_sds, n_repetitions,seed, n_obs)
        
    assert "Parameter cannot be a string." == str(excinfo.value)    

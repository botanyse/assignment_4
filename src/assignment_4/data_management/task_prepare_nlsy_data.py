"""Tasks for managing the data."""

from pathlib import Path

import pytask
import pandas as pd

from assignment_4.config import BLD, SRC
from assignment_4.data_management.clean_chs_nlsy_data import clean_and_reshape_nlsy_data

prepare_nlsy_deps = {
    "scripts": Path("clean_chs_nlsy_data.py"),
    "data_info": BLD / "python" / "data" / "original_data" / "bpi_variable_info.csv",
    "data": BLD / "python" / "data" / "original_data" /
    "BEHAVIOR_PROBLEMS_INDEX.dta",
}

def task_prepare_nlsy_data(
    depends_on=prepare_nlsy_deps,
    produces=BLD / "python" / "data" / "clean_nlsy_data.arrow",
):
    raw = pd.read_stata(depends_on['data'])
    info = pd.read_csv(depends_on['data_info'])
    cleaned_data = clean_and_reshape_nlsy_data(raw=raw, info=info)
    cleaned_data.to_feather(produces)

"""Tasks for managing the data."""

from pathlib import Path

import pytask
import pandas as pd

from assignment_4.config import BLD, SRC
from assignment_4.data_management.clean_chs_nlsy_data import clean_chs_data

prepare_chs_deps = {
    "scripts": Path("clean_chs_nlsy_data.py"),
    "data": BLD / "python" / "data" / "original_data" / "chs_data.dta",
}

def task_prepare_chs_data(
        depends_on = prepare_chs_deps,
        produces = BLD / "python" / "data" / "clean_chs_data.arrow",
):
    """Clean chs data."""
    raw = pd.read_stata(depends_on["data"])
    cleaned_data = clean_chs_data(raw)
    cleaned_data.to_feather(produces)
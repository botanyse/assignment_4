from pathlib import Path

import pandas as pd

from assignment_4.config import BLD
from assignment_4.data_management.merge_chs_nlsy_data import merge_df

merge_data_deps = {
    "scripts": Path("merge_chs_nlsy_data.py"),
    "clean_chs_data": BLD / "python" / "data" / "clean_chs_data.arrow",
    "clean_nlsy_data": BLD / "python" / "data" / "clean_nlsy_data.arrow",
}


def task_merge_chs_nlsy_data(
    depends_on=merge_data_deps,
    produces=BLD / "python" / "data" / "merged_chs_nlsy_data.csv",
):
    "Merge the data."
    clean_chs_data = pd.read_feather(depends_on["clean_chs_data"])
    clean_nlsy_data = pd.read_feather(depends_on["clean_nlsy_data"])
    merged_data = merge_df(clean_chs_data, clean_nlsy_data)
    merged_data.to_csv(produces)

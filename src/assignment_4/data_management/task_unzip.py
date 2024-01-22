import zipfile

from assignment_4.config import BLD, SRC

zipped_data = SRC / "data" / "original_data.zip"
bld_dir = BLD / "python" / "data" / "original_data"

produces = [
    bld_dir / "BEHAVIOR_PROBLEMS_INDEX.cdb",
    bld_dir / "BEHAVIOR_PROBLEMS_INDEX.dta",
    bld_dir / "bpi_variable_info.csv",
    bld_dir / "chs_data.dta",
]


def task_unzip(raw_file=zipped_data, produces=produces):
    """Extract the files from the zip file."""
    with zipfile.ZipFile(raw_file, "r") as zip_ref:
        return zip_ref.extractall(bld_dir)

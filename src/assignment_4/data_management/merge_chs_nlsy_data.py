import pandas as pd

pd.options.mode.copy_on_write = True
pd.options.future.infer_string = True
pd.options.plotting.backend = "plotly"


def merge_df(clean_chs, clean_nlys):
    """Merges two dataframes on their indices, drops the 'momiddrop' column, and filters
    rows based on the 'age' column.

    Args:
        clean_chs (pandas.DataFrame): The first dataframe to merge.
        clean_nlys (pandas.DataFrame): The second dataframe to merge.

    Returns:
        pandas.DataFrame: The merged dataframe with rows where 'age' is between 5 and 13 (inclusive).

    """
    clean_merged = pd.merge(
        clean_chs,
        clean_nlys,
        left_index=True,
        right_index=True,
        how="left",
        suffixes=(None, "drop"),
    )
    clean_merged = clean_merged.drop(columns="momiddrop")
    return clean_merged[(clean_merged["age"] <= 13) & (clean_merged["age"] >= 5)]

import pandas as pd

pd.options.mode.copy_on_write = True
pd.options.future.infer_string = True
pd.options.plotting.backend = "plotly"

def merge_df(clean_chs,clean_nlys):
    clean_merged = pd.merge(clean_chs,clean_nlys,left_index=True, right_index=True, how='left', suffixes= (None, 'drop'))
    clean_merged = clean_merged.drop(columns='momiddrop')
    clean_merged = clean_merged[(clean_merged['age']<=13) & (clean_merged['age']>=5)]
    return clean_merged
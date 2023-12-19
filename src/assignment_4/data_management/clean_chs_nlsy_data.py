"""Functions for cleaning the datasets"""
import pandas as pd

pd.options.mode.copy_on_write = True
pd.options.future.infer_string = True
pd.options.plotting.backend = "plotly"

def clean_chs_data(raw): 
    """Clean 'raw' DataFrame, create a new DataFrame with the same index as 'raw' and fill in with cleaned columns of 'raw'.
    Function involves replacing negative values of columns from 'bpiA' to 'bpiE' are with pd.NA, changing datatypes of 'momid','age','childid','year', and setting 'childid' and 'year' as index.
    
    Args:
        raw (pd.DataFrame): Raw data to be cleaned.

    Returns:
        df (pd.DataFrame): The cleaned data.
    """
    mapping_dict = {
    'not true': 0,
    'sometimes true': 1,
    'often true': 1
    }

    df = pd.DataFrame(index = raw.index)
    df["momid"] = (raw["momid"]).astype(pd.UInt32Dtype())
    df["age"] = (raw["age"]).astype(pd.UInt32Dtype())
    for i in ["bpiA", "bpiB", "bpiC", "bpiD", "bpiE"]:
        df[i] = _clean_bpi(raw[i]).astype(pd.Float32Dtype())
    df = df.set_index([(raw["childid"]).astype(pd.UInt32Dtype()), (raw["year"]).astype(pd.UInt32Dtype())])
    return df

def _clean_bpi(sr):
    """Replace BPI values '-100' with pd.NA."""
    sr = sr.replace({-100.000000: pd.NA})
    return sr

##-----------------------------------------------------------------##

def clean_and_reshape_nlsy_data(raw, info):
    cleaned_yearly_data = [clean_year_data(raw,i, info) for i in range(1986,2011,2)]
    return pd.concat(cleaned_yearly_data)

def clean_year_data(raw, year, info):
    mapping_dict = {
    'not true': 0,
    'sometimes true': 1,
    'often true': 1
    }
    
    df = pd.DataFrame(index=raw.index)
    for i in raw.columns[:3]:
        df[i] = raw[i]
    year_list = _filter_by_year(raw,year,info)
    df[year_list] = raw[year_list]
    df['year'] = year
    df = _clean_bpi_variables(df,info)
    df["childid"] = df["childid"].astype(pd.UInt32Dtype())
    df["momid"] = df["momid"].astype(pd.UInt32Dtype())
    df["birth_order"] = df["birth_order"].cat.codes
    df  = df.set_index(["childid","year"])
    for i in df.columns[2:]:
        df[i] = _clean_bpi_cat(df[i])
    
    df = pd.concat([df, _add_subscale_scores(df, mapping_dict)], axis=1)
    return df.sort_index()

def _filter_by_year(raw_df,year,info):
    info_by_year = info.loc[info.survey_year == str(year)]
    nlsy_by_year = info_by_year.loc[:,"nlsy_name"].to_list()
    return nlsy_by_year

def _clean_bpi_variables(df, info_df):
     clean_variables = dict(zip(info_df.nlsy_name, info_df.readable_name)) # creating a dictionary to rename columns in raw data
     return df.rename(columns=clean_variables)

def _clean_bpi_cat(sr):
    sr = sr.replace([-7.0, -3.0, -2.0, -1.0], pd.NA)
    sr = sr.replace({'Never Attended School': pd.NA, 'Multiple selection': pd.NA })
    categories = ["not true", "sometimes true", "often true"]
    sr = sr.astype(pd.StringDtype()).str.lower().astype(pd.CategoricalDtype(categories=categories, ordered=True))
    return sr

def _add_subscale_scores(df ,dict):
    subscale = df.copy()
    for i in subscale.columns[2:]:
        subscale[i] = subscale[i].map(dict)
    
    categories = ["antisocial", "anxiety", "headstrong", "hyperactive", "dependence","peer"]
    for i in categories:
        subscale[i] = subscale[[col for col in subscale.columns if col.startswith(i)]].mean(axis=1)
    subscale = subscale[categories]
    return subscale


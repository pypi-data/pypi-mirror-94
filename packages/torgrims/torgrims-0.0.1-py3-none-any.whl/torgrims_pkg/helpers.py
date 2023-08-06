import pandas as pd
import numpy as np
from typing import List

def catcol(df:pd.DataFrame, col:str)->pd.DataFrame:
    '''
    Generate stats for single categorical column in dataframe
    '''

    return pd.DataFrame({
        'n_obs':df[col].value_counts(dropna=False),
        'freq':df[col].value_counts(dropna=False, normalize=True)
    })

def catcol_response(df:pd.DataFrame, col:str, response:str)->pd.DataFrame:
    '''
    Generate stats for single categorical column in dataframe.
    Compare with response
    '''
    return pd.DataFrame({
        'n_obs':df[col].value_counts(dropna=False),
        'freq':df[col].value_counts(dropna=False, normalize=True),
        'mean_response':df.groupby(col)[response].mean()
    })


def correl_(df:pd.DataFrame, x:str,y:str)->float:
    try:
        return np.corrcoef(df[x],df[y])[0,1]
    except:
        return np.nan

NULLISH=[np.nan, 0, -999, 'missing', '?', '', ' ', '  ', '   ']
def stats(df:pd.DataFrame, nullish:List=NULLISH, response='target')->pd.DataFrame:
    '''
    Generate statistics for pandas dataframe
    '''
    return pd.DataFrame({
        'dtype':df.dtypes,
        'corr_response':pd.Series({c:correl_(df,response,c) for c in df.columns}),
        'cardinality':df.nunique(),
        'n_nullish':df.isin(nullish).sum(),
        'pos_outlier_count':(df > df.quantile(.75)+1.5*(df.quantile(.75)-df.quantile(.25))).sum(),                    
        'neg_outlier_count':(df < df.quantile(.25)-1.5*(df.quantile(.75)-df.quantile(.25))).sum(),         
        'mean':df.mean(),
        'p_50':df.quantile(.50, axis=0),
        'std':df.std(),
        'min':df.min(),
        'max':df.max(),
        'kurtosis':df.kurt(),
        'skewness':df.skew(),    
        'p_05':df.quantile(.05, axis=0),
        'p_10':df.quantile(.10, axis=0),
        'p_25':df.quantile(.25, axis=0),        
        'p_75':df.quantile(.75, axis=0),
        'p_90':df.quantile(.90, axis=0),
        'p_95':df.quantile(.95, axis=0),
    })
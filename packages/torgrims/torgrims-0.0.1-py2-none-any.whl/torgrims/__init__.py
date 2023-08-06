import pandas as pd
import numpy as np
from typing import List, Dict, Union
from __future__ import annotations
from pandas.core.tools import numeric
from scipy.stats import boxcox

class DescStat():

    NULLISH=[np.nan, 0, -999, 'missing', '?', '', ' ', '  ', '   ']

    @staticmethod
    def correl(df:pd.DataFrame, x:str,y:str)->float:
        try:
            return np.corrcoef(df[x],df[y])[0,1]
        except:
            return np.nan


    @staticmethod
    def catcol(df:pd.DataFrame, col:str)->pd.DataFrame:
        '''
        Generate stats for single categorical column in dataframe
        '''
        return pd.DataFrame({
            'n_obs':df[col].value_counts(),
            'freq':df[col].value_counts(normalize=True),
            'n_missing':df.groupby(col)[col].count().rsub(df.groupby(col)[col].size(), axis=0),
            'pct_tot_missing': df.groupby(col)[col].count().rsub(df.groupby(col)[col].size(), axis=0)/df.shape[0]
        }).T  

    @staticmethod
    def catcol_response(df:pd.DataFrame, col:str, response:str)->pd.DataFrame:
        '''
        Generate stats for single categorical column in dataframe.
        Compare with response
        '''
        return pd.DataFrame({
            'mean_response':df.groupby(col)[response].mean(),
            'n_obs':df[col].value_counts(),
            'freq':df[col].value_counts(normalize=True),
            'n_missing':df.groupby(col)[col].count().rsub(df.groupby(col)[col].size(), axis=0),
            'pct_tot_missing': df.groupby(col)[col].count().rsub(df.groupby(col)[col].size(), axis=0)/df.shape[0]
        }).T        

    @staticmethod
    def numcol(df:pd.DataFrame, col:str, nullish:List=NULLISH)->pd.DataFrame:
        '''
        Generate stats for single numerical column in dataframe
        '''
        q25 = df[col].quantile(.25)
        q75 = df[col].quantile(.75)
        IQR = q75-q25
        stats_frame =  pd.DataFrame({            
            'mean':[df[col].mean()],
            'min':[df[col].min()],
            'p25':[df[col].quantile(.25)],
            'p50':[df[col].quantile(.5)],
            'p75':[df[col].quantile(.75)],
            'max':[df[col].max()],
            'skew(pos=right tail)':[df[col].skew()],
            'fisher_kurtosis(pos=thick tail)':[df[col].kurt()],
            'neg_outlier_threshold':[q25-1.5*IQR],
            'neg_outliers': [df.loc[df[col]<(q25-1.5*IQR),col].shape[0]],
            'pos_outlier_threshold':[q75+1.5*IQR],
            'pos_outliers': [df.loc[df[col]>(q75+1.5*IQR),col].shape[0]],
            'n_nan': [df[col].isin([np.nan]).sum()],
            'n_nullish': [df[col].isin(nullish).sum()],
            'pct_tot_nullish': [df[col].isin(nullish).sum()/df.shape[0]],
            'dtype':[df[col].dtype]
        }).T
        stats_frame.columns=[col]
        return stats_frame

    @staticmethod
    def numcol_response(df:pd.DataFrame, col:str, response:str, nullish:List=NULLISH)->pd.DataFrame:
        '''
        Generate stats for single numerical column in dataframe
        '''
        stats_frame=DescStat.numcol(df, col)
        response_frame=pd.DataFrame({
            'correl_response':[DescStat.correl(df, col, response)],
            'std':[df[col].std()],
        }).T
        response_frame.columns=[col]
        return pd.concat([response_frame, stats_frame], axis=0)

    @staticmethod
    def dfstats(df:pd.DataFrame, nullish:List=NULLISH, response='target')->pd.DataFrame:
        '''
        Generate statistics for pandas dataframe
        '''
        return pd.DataFrame({
            'dtype':df.dtypes,
            'corr_response':pd.Series({c:DescStat.correl(df,response,c) for c in df.columns}),
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

from sklearn.base import BaseEstimator, TransformerMixin
class FeatureSelectTransformer(BaseEstimator, TransformerMixin):
    '''
    Transformer to select feature from frame
    '''
    def __init__(self, col:Union[str,List[str]])->None:
        super().__init__()
        if type(col)==str:
            col = [col]
        assert len(col)==1, 'Only one feature accepted'
        self.col = col

    def fit(self, X:pd.DataFrame, y:pd.DataFrame=None)->FeatureSelectTransformer:
        return self

    def transform(self, X:pd.DataFrame, y:pd.DataFrame=None)->pd.DataFrame:
        X=X.copy()
        return X[self.col]

class ToTypeTransformer(BaseEstimator, TransformerMixin):
    '''
    Cast col to proper type, np.nan on error
    '''
    def __init__(self, type:str, date_format:str='%Y-%m-%d')->None:
        self.type=type
        self.date_format=date_format

    def fit(self, X:pd.DataFrame, y:pd.DataFrame=None)->ToTypeTransformer:
        return self

    def transform(self, X:pd.DataFrame, y:pd.DataFrame=None)->pd.DataFrame:
        X=X.copy()
        for c in X.columns:
            if self.type=='numeric':
                X[c] = pd.to_numeric(X[c], errors='coerce')
            if self.type=='string':
                X[c] = X[c].astype(str)
            if self.type=='date':
                X[c] = pd.to_datetime(X[c], format=self.date_format, errors='coerce')
            return X           

class ToOrdinalTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, mapping_dict:Dict={}):
        self.mapping_dict=mapping_dict.copy()

    def fit(self, X:pd.DataFrame, y:pd.DataFrame=None)->ToOrdinalTransformer:
        X=X.copy()
        if not self.mapping_dict:
            assert X.shape[1]==1, 'Transformer support only one column'
            columns=list(X.columns)
            for c in columns:
                self.mapping_dict[c] = {
                    e[0]:e[1] for e in zip(
                        X[c].unique(),
                        range(len(X[c].unique()))
                    )
                }
        return self

    def transform(self, X:pd.DataFrame, y:pd.DataFrame=None)->pd.DataFrame:
        X = X.copy()
        for k in self.mapping_dict.keys():
            X[k] = X[k].map(self.mapping_dict[k])
        return X

    def inverse_transform(self, X, y=None):
        X = X.copy()
        for v in self.mapping_dict.keys():
            inverse_map = {
                v:k for k,v in self.mapping_dict[v].items()
            }
            X[v] = X[v].map(inverse_map)
        return X        
    
class ImputeTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, strategy:str='mean', fillvalue=np.nan, fillvalue_map:Dict={}):
        super().__init__()
        self.strategy=strategy
        self.fillvalue=fillvalue
        self.fillvalue_map=fillvalue_map.copy()

    def fit(self, X:pd.DataFrame, y:pd.DataFrame=None):
        if not self.fillvalue_map:
            for c in X.columns:
                if self.strategy == 'mean':    
                    self.fillvalue_map[c]={
                        'fill_value':X[c].mean()
                    }
                if self.strategy == 'median':    
                    self.fillvalue_map[c]={
                        'fill_value':X[c].quantile(.5)
                    }   
                if self.strategy == 'constant':
                    self.fillvalue_map[c]={
                        'fill_value':self.fillvalue
                    }                     
        return self

    def transform(self, X:pd.DataFrame, y:pd.DataFrame=None):
        X=X.copy()
        for c in X.columns:
            X[c]=X[c].replace(np.nan, self.fillvalue_map[c]['fill_value'])
        return X
    
class NullishToNanTransformer(BaseEstimator, TransformerMixin):

    NULLISH=[np.nan, 0, -999, 'missing', '?', '', ' ', '  ', '   ']
    def __init__(self, null_def:List[Union[str,int,float]]=NULLISH):
        super().__init__()
        self.null_def=null_def

    def fit(self, X:pd.DataFrame, y:pd.DataFrame=None):
        return self

    def transform(self, X:pd.DataFrame, y:pd.DataFrame=None):
        X=X.copy()
        for c in X.columns:
            X.loc[X[c].isin(self.null_def), c]=np.nan
        return X

class RemoveOutliersTransformer(BaseEstimator, TransformerMixin):
    'replace values of outliers to either bound or np.nan'
    def __init__(self, method='to_bound', threshold_map:Dict={}):
        self.method=method
        self.threshold_map=threshold_map.copy()

    def fit(self, X, y=None):
        if not self.threshold_map:
            for c in X.columns:
                p75=X[c].quantile(0.75)
                p25=X[c].quantile(0.25)
                lb = p25-1.5*(p75-p25)
                ub = p75+1.5*(p75-p25)                
                self.threshold_map[c]={
                    'lb':lb,
                    'ub':ub
                }
        return self

    def transform(self, X, y=None):
        X=X.copy()
        for c in X.columns:
            lb=self.threshold_map[c]['lb']
            ub=self.threshold_map[c]['ub']

            if self.method == 'to_bound':    
                X[c] = np.where(X[c] < lb, lb, X[c])
                X[c] = np.where(X[c] > ub, ub, X[c])
            else:
                X[c] = np.where(X[c] < lb, np.nan, X[c])
                X[c] = np.where(X[c] > ub, np.nan, X[c])
        return X


class OnehotTransformer(BaseEstimator, TransformerMixin):
    def __init__(self):
        super().__init__()
        self.unique_value_map={}

    def format_colname(self,c):
        return c.lstrip().rstrip().lower().replace('-','_') 

    def fit(self, X:pd.DataFrame, y:pd.DataFrame=None):
        for c in X.columns:
            self.unique_value_map[c]=list(X[c].unique())
        return self

    def transform(self, X:pd.DataFrame, y:pd.DataFrame=None):
        X = X.copy()
        for k,v in self.unique_value_map.items():
            ohe=pd.DataFrame({
                f'{k}_{self.format_colname(e)}':
                    np.where(X[k]==e, 1,0) for e in v
            })    
            X=pd.concat([X,ohe], axis=1)
            X.drop(k, axis=1, inplace=True)
        return X


class StdScalerTransformer(BaseEstimator, TransformerMixin):
    def __init__(self):
        super().__init__()
        self.scaler_map={}

    def fit(self, X:pd.DataFrame, y:pd.DataFrame=None)->pd.DataFrame:        
        for c in X.columns:
            self.scaler_map[c]={
                'mu':X[c].mean(),
                'std':X[c].std()
            }   
        return self

    def transform(self, X:pd.DataFrame, y:pd.DataFrame=None):
        X = X.copy()
        for c in X.columns:
            mu=self.scaler_map[c]['mu']
            std=self.scaler_map[c]['std']
            X[c]=(X[c]-mu)/std
        return X


class MinMaxScalerTransformer(BaseEstimator, TransformerMixin):
    def __init__(self):
        super().__init__()
        self.scaler_map={}

    def fit(self, X:pd.DataFrame, y:pd.DataFrame=None)->pd.DataFrame:        
        for c in X.columns:
            self.scaler_map[c]={
                'min':X[c].min(),
                'max':X[c].max()
            }   
        return self

    def transform(self, X:pd.DataFrame, y:pd.DataFrame=None):
        X = X.copy()
        for c in X.columns:
            min=self.scaler_map[c]['min']
            max=self.scaler_map[c]['max']
            X[c]=(X[c]-min)/(max-min)
        return X

class BoxCoxScalerTransformer(BaseEstimator, TransformerMixin):
    def __init__(self):
        super().__init__()
        self.scaler_map={}

    def fit(self, X:pd.DataFrame, y:pd.DataFrame=None)->pd.DataFrame:        
        for c in X.columns:
            _,l=boxcox(df['Age'])
            self.scaler_map[c]={
                'lambda':l
            }   
        return self

    def transform(self, X:pd.DataFrame, y:pd.DataFrame=None):
        X = X.copy() 
        for c in X.columns:    
            l=self.scaler_map[c]['lambda']
            X[c]=boxcox(X[c],l)
        return X
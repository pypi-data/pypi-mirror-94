import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re

class Error(Exception):
    pass
class CorrelationError(Error):
    pass

''' 
The data_preparation methods can be used without an instance of a class over a DataFrame
'''

def col_cast(
    self,
    df,
    columns=[],
    to_cast=None
):
    r'''
    Return a dataframe with a set of columns casted.
    
    THIS METHOD HAS BE TESTED
    
    Parameters
    ----------
        self: Datup
            It is the object type Datup necessary to download using aws credentials and write the log. The 
            default folder for log is /tmp/
        df: DataFrame
            It is the DataFrame with which want to work
        columns: list, default None
            A list of columns which want to cast
        to_cast: str, default None
            The type of cast as str, int, float, etc.

    :return: A DataFrame with columns casted
    :rtype: DataFrame

    Examples
    --------
    >>> import datup as dt
    >>> dt.col_cast(object,df,["columns","to","cast"],"type of cast")
    ''' 

    try:
        for column in columns:
            df[column] = df[column].astype(to_cast)
    except IOError as error:        
        self.logger.exception(f"Exception found: {error}") 
        raise
    return df

def featureselection_correlation(
    self,
    df,
    method="spearman",
    thresold=0.7
):
    r''' 
    Return a graph with correlation factors between features and a list of features to drop as a suggest

    THIS METHOD HAS BE TESTED

    Parameters
    ----------
        self: Datup
                It is the object type Datup necessary to download using aws credentials and write the log. The 
                default folder for log is /tmp/
        df: DataFrame
            It is the DataFrame with which want to work
        method: str, default 'spearman'
            Took it from Pandas corr methods description
            Method of correlation:
                pearson : standard correlation coefficient
                kendall : Kendall Tau correlation coefficient
                spearman : Spearman rank correlation
                callable: callable with input two 1d ndarrays 
                    and returning a float. Note that the returned matrix from corr will have 1 along the diagonals
                    and will be symmetric regardless of the callable’s behavior.
        threshold: float, default 0.7
            Is the threshold of correlation factor which goes from 0 to 1

    :return: A Graph with correlation factors between features
    :rtype: Graph
    :return: A list with features that doesn't contribute with additional information to drop
    :rtype: List

    Examples
    --------
    >>> import datup as dt
    >>> dt.featureselection_correlation(object,df)
    '''

    try:
        object_list = []
        for column in df.columns:
            if df[column].dtype == "object":
                object_list.append(column)

        if len(object_list) > 0:
            raise CorrelationError("Is necessary convert the nex columns to a numeric representation: {}".format(object_list))
        else:
            corr_dor = df.corr(method=method).abs()
            upper_corr = corr_dor.where(np.triu(np.ones(corr_dor.shape), k=1).astype(np.bool))
            v_return = [dim for dim in upper_corr.columns if any(upper_corr[dim] > thresold)]
            fig = plt.figure(figsize=(10, 7.5))
            plt.matshow(corr_dor, fignum=fig.number)
            plt.xticks(range(df.shape[1]), df.columns, fontsize=11, rotation=90)
            plt.yticks(range(df.shape[1]), df.columns, fontsize=11)
            cb = plt.colorbar()
            cb.ax.tick_params(labelsize=11)
            plt.show()
    except CorrelationError as error:
        self.logger.exception(f"Exception found: {error}") 
        raise
    return v_return

def remove_chars_metadata(
    self,
    df
):
    '''
    Return a dataframe with columns names without special characters
    
    THIS METHOD HAS BE TESTED

    Parameters
    ----------
        self: Datup
            It is the object type Datup necessary to download using aws credentials and write the log. The 
            default folder for log is /tmp/
        df: DataFrame
            It is the DataFrame with which want to work
    
    :return: A DataFrame with columns cleaned
    :rtype: DataFrame

    Examples
    --------
    >>> import datup as dt
    >>> dt.remove_chars_metadata(object,df)
    '''
    try:
        to_remove = ['/','\\(','\\)','\\?',',','\\n',':','\\.','\\t']
        dims = [re.sub('|'.join(to_remove),'', dim) for dim in df.columns]
        dims = [re.sub(' ','_', col) for col in dims]
        dims = [re.sub('á','a', col) for col in dims]
        dims = [re.sub('é','e', col) for col in dims]
        dims = [re.sub('í','i', col) for col in dims]
        dims = [re.sub('ó','o', col) for col in dims]
        dims = [re.sub('ú','u', col) for col in dims]
        dims = [re.sub('ñ','n', col) for col in dims]
        dims = [re.sub('Á','A', col) for col in dims]
        dims = [re.sub('É','E', col) for col in dims]
        dims = [re.sub('Í','I', col) for col in dims]
        dims = [re.sub('Ó','O', col) for col in dims]
        dims = [re.sub('Ú','U', col) for col in dims]
        dims = [re.sub('Ñ','N', col) for col in dims]
        dims = [re.sub('Ã“','O', col) for col in dims] 
        dims = [re.sub('Ã³','o', col) for col in dims]
        dims = [re.sub('Ã¡','a', col) for col in dims]
        dims = [re.sub('Ã','i', col) for col in dims]
        dims = [re.sub('Ãº','u', col) for col in dims]
        dims = [re.sub('Ã±','ni', col) for col in dims]
        dims = [re.sub('\\$','cop', col) for col in dims]
        dims = [re.sub('%','pct_', col) for col in dims]
        dims = [re.sub('#','_num', col) for col in dims]
        df.columns=dims
    except IOError as error:
        self.logger.exception(f'Exception found: {error}')
        raise 
    return df

def to_lowercase_metadata(
    self,
    df
):
    '''
    Return a dataframe with columns in lowercase
    
    THIS METHOD HAS BE TESTED

    Parameters
    ----------
        self: Datup
            It is the object type Datup necessary to download using aws credentials and write the log. The 
            default folder for log is /tmp/
        df: DataFrame
            It is the DataFrame with which want to work
    
    :return: A DataFrame with lowercased columns 
    :rtype: DataFrame

    Examples
    --------
    >>> import datup as dt
    >>> dt.to_lowercase_metadata(object,df)
    '''
    try:
        dims = [dim.lower() for dim in df.columns]
        df.columns = dims
    except IOError as error:
        self.logger.exception(f'Exception found: {error}')
        raise 
    return df

def profile_dataset(self,df):
    '''
    Return a dataframe of all dimensions with its domain values and their occurrences (frequencies)
    
    THIS METHOD HAS BE TESTED

    Parameters
    ----------
        self: Datup
            It is the object type Datup necessary to download using aws credentials and write the log. The 
            default folder for log is /tmp/
        df: DataFrame
            It is the DataFrame with which want to work
    
    :return: A DataFrame with its domain values and their occurrences (frequencies) 
    :rtype: DataFrame

    Examples
    --------
    >>> import datup as dt
    >>> dt.profile_dataset(object,df)    
    '''

    try:
        profile_list = []
        num_dims = len(df.columns)
        for idx, dim in enumerate(df.columns):
            dims = []
            values = list(df[dim].value_counts().index.astype('str'))
            freqs = list(df[dim].value_counts().values.astype('int64'))
            [dims.append(dim) for i in range(len(values))]    
            dims_values_freqs = list(zip(dims, values, freqs))    
            profile_list += dims_values_freqs    
            self.logger.debug('{predictor} completed {dim_id}/{num_dims})...'.format(predictor=dim, dim_id=idx+1, num_dims=num_dims))
            df_profile = pd.DataFrame(profile_list, columns=['Dimension', 'Value', 'Frequency'])
    except IOError as error:
        self.logger.exception(f'Exception found: {error}')
        raise 
    return df_profile

def rank_sku_abc(
    df,
    sort_dim,
    abc_thres_list=[0.8, 0.95, 1.1]
):
    """
    Return a dataframe ranking the SKUs in ABC classes based on the  sorting dimension

    Parameters
    __________
    df: DataFrame
        It is the DataFrame with which want to work
    sort_dim: str
        Is the dataframe's dimension to classify the SKUs (e.g. quantity, costs, revenues)
    abc_thers_list: list
        Is the list of thresholds to classify SKU into A, B or C

    :return: A DataFrame with SKUs ranked as ABC
    :rtype: DataFrame

    Examples
    --------
    >>> import datup as dt
    >>> dt.rank_sku_abc(df,sort_dim,abc_thres_list)
    """
    try:
        df_abc = df.sort_values([sort_dim+' sum'], ascending=False).reset_index(drop=True)
        df_abc[sort_dim+' sum Pct'] = df_abc[sort_dim+' sum']/df_abc[sort_dim+' sum'].sum()
        df_abc[sort_dim+' sum Pct Acum'] = df_abc[sort_dim+' sum Pct'].cumsum()
        df_abc.loc[df_abc[sort_dim+' sum Pct Acum']<=abc_thres_list[0],'ABC'] = 'A'
        df_abc.loc[(df_abc[sort_dim+' sum Pct Acum']>abc_thres_list[0]) & (df_abc[sort_dim+' sum Pct Acum']<=abc_thres_list[1]),'ABC'] = 'B'
        df_abc.loc[(df_abc[sort_dim+' sum Pct Acum']>abc_thres_list[1]) & (df_abc[sort_dim+' sum Pct Acum']<=abc_thres_list[2]),'ABC'] = 'C'
    except IOError as error:
        print(f'Exception found: {error}')
        raise
    return df_abc

def rank_sku_xyz(
    df,
    sort_dim,
    xyz_thres_list=[0.33, 0.66]
):
    """
    Return a dataframe ranking the SKUs in XYZ classes based on the  sorting dimension

    Parameters
    __________
    df:
        It is the DataFrame with which want to work
    sort_dim:
        Is the dataframe's dimension to classify the SKUs (e.g. quantity, costs, revenues)
    xyz_thres_list:
        Is the list of thresholds to classify SKU into X, Y or Z

    :return: A DataFrame with SKUs ranked as XYZ
    :rtype: DataFrame

    Examples
    --------
    >>> import datup as dt
    >>> dt.rank_sku_xyz(df,sort_dim,xyz_thres_list)
    """
    try:
        xyz_list = []
        df[sort_dim+' std Pct'] = (df[sort_dim+' std']/df[sort_dim+' mean']).fillna(0)
        for val in df[sort_dim+' std Pct'].values:
            if val <= xyz_thres_list[0]: xyz_list.append('X')
            elif val > xyz_thres_list[0] and val <= xyz_thres_list[1]: xyz_list.append('Y')
            else: xyz_list.append('Z')
        df['XYZ'] = xyz_list
    except IOError as error:
        print(f'Exception found: {error}')
        raise
    return df

def rank_sku_fsn(
    df,
    sort_dim,
    fsn_thres_list=[0.5, 0.75]
):
    """
    Return a dataframe ranking the SKUs in FSN classes based on the sorting dimension

    Parameters
    __________
    df:
        It is the DataFrame with which want to work
    sort_dim:
        Is the dataframe's dimension to classify the SKUs (e.g. quantity, costs, revenues)
    fsn_thres_list:
        Is the list of thresholds to classify SKU into F, S or N

    :return: A DataFrame with SKUs ranked as FSN
    :rtype: DataFrame

    Examples
    --------
    >>> import datup as dt
    >>> dt.rank_sku_fsn(df,sort_dim,fsn_thres_list)
    """
    try:
        fsn_list = []
        for val in df[sort_dim+' run'].values:
            if val <= fsn_thres_list[0]: fsn_list.append('N')
            elif val > fsn_thres_list[0] and val <= fsn_thres_list[1]: fsn_list.append('S')
            else: fsn_list.append('F')
        df['FSN'] = fsn_list
    except IOError as error:
        print(f'Exception found: {error}')
        raise
    return df

def replace_categorical_na(
    self,
    df,
    na_value
):
    '''
    Returns a dataframe without na values in categorical dimensions

    THIS METHOD HAS BE TESTED

    Parameters
    ----------
        self: Datup
            It is the object type Datup necessary to download using aws credentials and write the log. The 
            default folder for log is /tmp/
        df: DataFrame
            It is the DataFrame with which want to work
        na_value: str
            It is the value to replace the NaN one

    :return: A DataFrame without na values in categorical dimensions 
    :rtype: DataFrame

    Examples
    --------
    >>> import datup as dt
    >>> dt.replace_categorical_na(object,df,na_values='ND')     
    '''

    try:
        categorical_dims = [dim for dim in df.columns if df[dim].dtype == object]
        for dim in categorical_dims:
            df[dim] = df[dim].fillna(value=na_value)
            na_flag = df[dim].isnull().values.any()
            self.logger.debug('{dimension} has NaNs: {flag}'.format(dimension=dim, flag=na_flag))                
    except IOError as error:
        self.logger.exception(f'Exception found: {error}')
        raise 
    return df

def replace_numeric_na(
    self,
    df,
    na_value
):
    '''
    Returns a dataframe without na values in numeric dimensions
    
    THIS METHOD HAS BE TESTED
    
    Parameters
    ----------
        self: Datup
            It is the object type Datup necessary to download using aws credentials and write the log. The 
            default folder for log is /tmp/
        df: DataFrame
            It is the DataFrame with which want to work
        na_value: int
            It is the value to replace the NaN one

    :return: A DataFrame without na values in numeric dimensions 
    :rtype: DataFrame

    Examples
    --------
    >>> import datup as dt
    >>> dt.replace_numeric_na(object,df,na_values=0)  
    '''
    
    try:
        numeric_dims = [dim for dim in df.columns if df[dim].dtype == 'float64' or df[dim].dtype == 'int64']
        for dim in numeric_dims:
            df[dim] = df[dim].fillna(value=na_value)    
            na_flag = df[dim].isnull().values.any()
            self.logger.debug('{dimension} has NaNs: {flag}'.format(dimension=dim, flag=na_flag))  
    except IOError as error:
        self.logger.exception(f'Exception found: {error}')
        raise 
    return df

def replace_datetime_na(self,df):
    """
    Returns a dataframe without na values in datetime dimensions
    
    THIS METHOD HAS BE TESTED
    
    Parameters
    ----------
        self: Datup
            It is the object type Datup necessary to download using aws credentials and write the log. The 
            default folder for log is /tmp/
        df: DataFrame
            It is the DataFrame with which want to work

    :return: A DataFrame without na values in datetime dimensions 
    :rtype: DataFrame

    Examples
    --------
    >>> import datup as dt
    >>> dt.replace_datetime_na(object,df,na_values=0)
    """
    try:
        datetime_dims = [dim for dim in df.columns if df[dim].dtype=='datetime64']
        for dim in datetime_dims:
            df[dim] = pd.to_datetime(df[dim], errors='coerce')    
            na_flag = df[dim].isnull().values.any()
            self.logger.debug('{dimension} has NaNs: {flag}'.format(dimension=dim, flag=na_flag))  
    except IOError as error:
        self.logger.exception(f'Exception found: {error}')
        raise 
    return df
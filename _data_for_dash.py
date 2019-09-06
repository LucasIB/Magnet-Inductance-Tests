from os import listdir
from os.path import isfile, join
import numpy as np
import pandas as pd

_CH_path = 'C:/Users/labimas/Documents/Lucas/Magnet-Inductance-Tests/Fast Correctors/FC-001/ch'
_CV_path = 'C:/Users/labimas/Documents/Lucas/Magnet-Inductance-Tests/Fast Correctors/FC-001/cv'
_QS_path = 'C:/Users/labimas/Documents/Lucas/Magnet-Inductance-Tests/Fast Correctors/FC-001/qs'

def handling_data(path):
    _files = [f for f in listdir(path) if isfile(join(path, f))]
    _f = []
    for item in _files:
        if '.csv' in item:
            _f.append(item)
    return _f, path

def create_main_dfs(arq): # arq = _f, path
    _dfs = []
    for i in range(len(arq[0])):
        _val = pd.read_csv(arq[1]+'/'+str(arq[0][i]), sep=',', header=1)
        _dfs.append(_val)
    return _dfs

def v_i_dfs(_dfs, option='i'):
    '''Build DFs for voltage and current, specifically'''
    _current_array = []
    _volts_array = []
    for df in _dfs:
        _volts_array.append(df.Volt.values)
        _current_array.append(df.Ampere.values)

    #Convert list in np.array
    _volts_array = np.asarray(_volts_array)
    _current_array = np.asarray(_current_array)
    
    #Transposed arrays
    _volts_array = _volts_array.T
    _current_array = _current_array.T

    #Creating respect DFs an add time column
    _df_volts = pd.DataFrame(_volts_array,
                             columns=['0-0.1A', '0-0.2A', '0-0.3A', '0-0.4A', '0-0.5A',
                                      '0-0.6A', '0-0.7A', '0-0.8A', '0-0.9A', '0-1A'],
                             index=_dfs[0].second)
    
    _df_current = pd.DataFrame(_current_array,
                               columns=['0-0.1A', '0-0.2A', '0-0.3A', '0-0.4A', '0-0.5A',
                                        '0-0.6A', '0-0.7A', '0-0.8A', '0-0.9A', '0-1A'],
                               index=_dfs[0].second)
    if option == 'i':
        return _df_current
    else:
        return _df_volts

def slice_df_interval(df, start, end):
    '''Slice the DF for specific interval'''
    return df[start:end]

def poly_fit_func(df, n): # n= polynomial order
    '''Find the polynomial fit for each current step'''
    _poly_array = []
    _deriv_array = []
    _x_axis = df.index
    for item in df.columns:
        #Fitting polynomial
        poly = np.polyfit(_x_axis,df[item],n)
        ploy1d = np.poly1d(poly)
        _poly_array.append(ploy1d)
        
        #Derivative curve
        _deriv = ploy1d.deriv()  #dI/dt
        _deriv_array.append(_deriv)
    
    _f = []
    for i in _deriv_array:
        final = np.array([])
        for j in _x_axis:
            final = np.append(final, i(j))
        _f.append(final)
    return _f

def df_creator(df,_derive_datas):
    '''Method for create DF with all steps'''
    _list_dfs = []
    for i in range(len(df.columns)):
        _dicionario = {'time(s)':df.index,
                       'I(A)':df[df.columns[i]].values,
                       'dI/dt': _derive_datas[i],
                       }
        _list_dfs.append(pd.DataFrame.from_dict(_dicionario))
    return _list_dfs

def derivative_from_data(_list_dfs):
    '''Numerical method for obtaining the derivative from raw data'''
    _x_axis = _list_dfs[0]['time(s)']
    _rd = []
    _raw_deriv = []
    for i in range(len(_list_dfs)):
        _rd.append(np.diff(_list_dfs[i]['I(A)']) / np.diff(_x_axis))
    for item in _rd:
        item = np.append(item, 0)
        _raw_deriv.append(item)
    return _raw_deriv

def export_list():
    '''Export DF list to dashboard app'''
    #DataFrame with all steps I and dI/dt:
    _files_i_ch = handling_data(_CH_path)
    _files_i_cv = handling_data(_CV_path)
    #Creating DFs for each step data:
    _dfs_ch = create_main_dfs(_files_i_ch)
    _dfs_cv = create_main_dfs(_files_i_cv)
    #Creating Current specific Dfs for CV and CH:
    _df_i_ch = v_i_dfs(_dfs_ch, 'i')
    _df_i_cv = v_i_dfs(_dfs_cv, 'i')
    #Slice Df for specific interval:
    a_ch = slice_df_interval(_df_i_ch, -0.001, 0.001)
    a_cv = slice_df_interval(_df_i_cv, -0.001, 0.001)
    #Creating derivative array for I in CV and CH:
    d_array_ch = poly_fit_func(a_ch, 25)
    d_array_cv = poly_fit_func(a_cv, 25)
    #Finally, list os DataFrames for each current step:
    _list_of_dfs_ch = df_creator(a_ch, d_array_ch)
    _list_of_dfs_cv = df_creator(a_cv, d_array_cv)

    return _list_of_dfs_ch, _list_of_dfs_cv

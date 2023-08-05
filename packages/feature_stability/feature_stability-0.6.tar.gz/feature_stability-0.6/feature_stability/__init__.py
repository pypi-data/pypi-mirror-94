#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
##  Function: Feature Importance Stability
##  Author: dj
##  Version: 1.0
##  Created on Tue Feb  4 11:22:58 2021

@author: juan.du
"""

## 导入所需模块包
import pandas as pd
import numpy as np
## 忽略警告信息
import warnings
warnings.filterwarnings('ignore')

#psi计算公式
def CalcBinPSI(x):
    if x.countRatio2 ==0 and x.countRatio1 == 0:
        PSI = 0
    elif x.countRatio1 == 0:
        PSI = 0.05
    else:
        PSI = (x.countRatio2 - x.countRatio1)*np.log(x.countRatio2*1.0 / x.countRatio1)
    return PSI 


# 生成lambda表达式，将连续变量粗分成约若干等份
def gen_lambda(binning,abnormal_values):
    temp = binning
    lambda_list = []
    for i in range(len(temp)):
        if i==0:
            lambda_list = 'lambda x: 0 if (x in %s) else %d if (x<=%f)'%(abnormal_values,temp.loc[i,'coarse_bin']+1,temp.loc[i,'ub'])
        elif i!=len(binning)-1:
            lambda_list = lambda_list + ' else %d if (x>%f) & (x<=%f)'%(temp.loc[i,'coarse_bin']+1,temp.loc[i,'lb'],temp.loc[i,'ub'])
        else:
            lambda_list = lambda_list + ' else %d if (x>%f) else np.nan'%(temp.loc[i,'coarse_bin']+1,temp.loc[i,'lb'])
    return lambda_list

##对于unique values>=5(可调整)的数值型变量，粗分成约5等份,异常值单独分箱
def coarse_bin(df_train,df_valid,exclude_column,bin_num=5,abnormal_values=[]):
    var_types = df_train.drop(exclude_column,axis=1).dtypes.reset_index()
    var_types.columns = ['var','type'] #float64, int64, object
    numeric_column = var_types[(var_types['type']=='float64')|(var_types['type']=='int64')]['var'].tolist()
    exclude_column = exclude_column + var_types[var_types['type']=='object']['var'].tolist()
    df_train_coarse_bin = df_train[exclude_column]
    df_valid_coarse_bin = df_valid[exclude_column]
#     coarse_bin_record = pd.DataFrame(columns=['var','coarse_bin','lb','ub']) ##记录各变量的binning区间
    for var in numeric_column:  
        if len(df_train[var].unique()) < bin_num:
#             print('No coarse binning for numeric variable %s as its unique values is less than 10'%(var))
            df_train_value=list(df_train[var].unique())
            lambda_list_train=[]
            if len(df_train_value)==1:
                lambda_list_train = 'lambda x: 0 if (x not in %s) else 1 if (x==%f) else np.nan'%(df_train_value,df_train_value[0])
            else:
                for i in range(len(df_train_value)):
                    if i==0:
                        lambda_list_train = 'lambda x: 0 if (x not in %s) else %d if (x==%f)'%(df_train_value,i+1,df_train_value[i])
                    elif i!=len(df_train_value)-1:
                        lambda_list_train = lambda_list_train + ' else %d if (x==%f)'%(i+1,df_train_value[i])
                    else:
                        lambda_list_train = lambda_list_train + ' else %d if (x==%f) else np.nan'%(i+1,df_train_value[i])
            df_train_coarse_bin[var] = list(map(eval(lambda_list_train),df_train[var]))
            df_valid_coarse_bin[var] = list(map(eval(lambda_list_train),df_valid[var]))
        else:
            df_train_noabn=df_train[~df_train[var].isin(abnormal_values)]
            split_values = df_train_noabn[var].quantile(np.linspace(0.1,0.9,num=bin_num)).reset_index()[var].unique()
#             print('Conduct coarse binning based on decile for numeric variable %s'%(var))
            binning = pd.DataFrame({'lb':[-99999]+split_values.tolist(),'ub':split_values.tolist()+[99999]}).reset_index()
            binning.rename(columns={'index':'coarse_bin'},inplace=True)
            binning['var'] = var
            binning = binning[['var','coarse_bin','lb','ub']]
#             coarse_bin_record = pd.concat([coarse_bin_record,binning],ignore_index=True)
            lambda_list = gen_lambda(binning,abnormal_values)
            df_train_coarse_bin[var] = list(map(eval(lambda_list),df_train[var]))
            df_valid_coarse_bin[var] = list(map(eval(lambda_list),df_valid[var]))
#     return data_coarse_bin,coarse_bin_record
    return df_train_coarse_bin,df_valid_coarse_bin

    
##计算两个数据集的psi
def calc_psi(df_train,df_valid,exclude_column,bin_num,abnormal_values):
    df_train_coarse_bin,df_valid_coarse_bin=coarse_bin(df_train,df_valid,exclude_column,bin_num,abnormal_values)
    h=[]
    for col in df_train.columns:
        if col not in exclude_column:
            df_train_bin_cnt=df_train_coarse_bin.groupby(col).size().reset_index().rename(columns={col:'bin',0:'count1'})
            df_train_bin_cnt['countRatio1']=df_train_bin_cnt['count1']/(df_train_coarse_bin[col].count())
            df_valid_bin_cnt=df_valid_coarse_bin.groupby(col).size().reset_index().rename(columns={col:'bin',0:'count2'})
            df_valid_bin_cnt['countRatio2']=df_valid_bin_cnt['count2']/(df_valid_coarse_bin[col].count())
            binInfo=pd.merge(df_train_bin_cnt,df_valid_bin_cnt,on='bin',how='inner')
            psi = sum(binInfo.apply(CalcBinPSI, axis=1))
            col_psi=[col,psi]
            h.append(col_psi)
    return pd.DataFrame(h,columns=['feature','psi'])


##计算多个数据集的psi的统计指标：最大／最小／平均／标准差，总体psi 
def calc_stat_psi(df_train,df_valid,exclude_column,bin_num,abnormal_values,datevar):
    dp_psiinfo=pd.DataFrame(columns=['date','feature','psi'])
    datelist=list(df_valid[datevar].unique())
    for date_str in datelist:
        df_valid_day=df_valid[df_valid[datevar]==date_str]
        dp_day=calc_psi(df_train,df_valid_day,exclude_column,bin_num,abnormal_values)
        dp_day['date']=date_str
        dp_psiinfo=dp_psiinfo.append(dp_day)
    dp_calcindex=dp_psiinfo.groupby('feature').agg({'psi':['max','min','mean','std']}).reset_index()
    psi_res=pd.DataFrame(columns=['feature','max_psi','min_psi','mean_psi','std_psi'])
    psi_res['feature']=dp_calcindex['feature']
    psi_res['max_psi']=dp_calcindex['psi']['max']
    psi_res['min_psi']=dp_calcindex['psi']['min']
    psi_res['mean_psi']=dp_calcindex['psi']['mean']
    psi_res['std_psi']=dp_calcindex['psi']['std']
    return psi_res

##结果合并
def Feature_stability(df_train,df_valid,exclude_column,bin_num,abnormal_values,datevar):
    psi_all=calc_psi(df_train,df_valid,exclude_column,bin_num,abnormal_values)
    psi_stat=calc_stat_psi(df_train,df_valid,exclude_column,bin_num,abnormal_values,datevar)
    psi_res=pd.merge(psi_all,psi_stat,on='feature',how='inner')
    return psi_res

if __name__ == '__main__':
    FFeature_stability(df_train,df_valid,exclude_column,bin_num,abnormal_values,datevar)


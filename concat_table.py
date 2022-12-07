# -*- coding: utf-8 -*-
"""
Created on Sun Oct 16 15:45:31 2022

@author: User
"""

import pandas as pd # 資料處理
import pyarrow as py 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


data = pd.read_parquet("airline_weather_concat_1019")


data_info = pd.DataFrame({'unicos':data.nunique(),
                          'missing_data':data.isna().mean()*100,
                          'dtype':data.dtypes})




plane_counts = data['Tail Number'].value_counts()

# plane_counts.index = [(item) for item in plane_counts.index]

commonPlane = plane_counts.iloc[:15].index

train_group = data.groupby('Tail Number')

# 這邊應該是在計算 delay 的機率，計算方法為先將所有的 tail number 全部加起來(利用 agg 聚合函數)，然後再用 mean 去計算平均
# https://zhuanlan.zhihu.com/p/101284491
train_mean_y = train_group['ArrDel15'].agg([lambda x:np.mean(x)])

fig, ax = plt.subplots(figsize=(20, 8))
# DataFrame.values屬性以返回給定DataFrame的numpy表示形式。
# 所以他會給定 每個 tail number 的值(values)
sns.barplot([it for it in commonPlane], train_mean_y.loc[commonPlane].values[:,0])
plt.xlabel('tail_number')
plt.ylabel('delay_probability')
plt.title('tailNumber result to delay')
plt.show()

# =============================================================================

Airport_counts = data['Dest'].value_counts()
Airport_counts_freq = Airport_counts / sum(Airport_counts)
# 點進去看會發現 他會按照順序
commonAirport = Airport_counts.iloc[:20].index
train_group = data.groupby('Dest')

train_mean_y = train_group['ArrDel15'].agg([lambda x:np.mean(x)])

fig, ax = plt.subplots(figsize=(12, 8)) 
sns.barplot(commonAirport, train_mean_y.loc[commonAirport].values[:,0])
plt.xlabel('Dest')
plt.ylabel('Delay_probability')
plt.title('Dest and Delay Relation')
plt.show()

# =============================================================================

Airport_counts = data['Origin'].value_counts()
Airport_counts_freq = Airport_counts / sum(Airport_counts)
# 點進去看會發現 他會按照順序
commonAirport = Airport_counts.iloc[:20].index
train_group = data.groupby('Origin')

train_mean_y = train_group['ArrDel15'].agg([lambda x:np.mean(x)])

fig, ax = plt.subplots(figsize=(12, 8)) 
sns.barplot(commonAirport, train_mean_y.loc[commonAirport].values[:,0])
plt.xlabel('Origin')
plt.ylabel('Delay Probability')
plt.title('Origin and Delay Relation')
plt.show()

fig, ax1 = plt.subplots(figsize=(12, 8))
# 共同的 x 軸具有不同的 y 軸。這是通過使用 twinx() 命令完成的。
ax2 = ax1.twinx() # ax2 and ax1 will have common x axis and different y axis
Airport_counts.loc[commonAirport].plot(kind='bar', ax=ax1, alpha=0.5)
train_mean_y.loc[commonAirport].plot(ax=ax2, color='r')
ax1.set_ylabel('times')
ax2.set_ylabel('Delay_probability')
handles1, labels1 = ax1.get_legend_handles_labels()
handles2, labels2 = ax2.get_legend_handles_labels()
labels1 = ['times']
labels2 = ['Delay_probability']
plt.legend(handles1+handles2, labels1+labels2, loc='upper right')
plt.show()

# =============================================================================

# 先取市占率 去看哪些值是我們值得看的
Company_counts = data['IATA_Code_Marketing_Airline'].value_counts()
Company_counts = Company_counts / Company_counts.sum()
commonCompany = Company_counts.index

# 依照 IATA 去分組
train_group = data.groupby('IATA_Code_Marketing_Airline')

# 把分組結果依照 ArrDel15 去
train_mean_y = train_group['ArrDel15'].agg([lambda x:np.mean(x)])

fig, ax = plt.subplots(figsize = (12, 8)) 
sns.barplot(commonCompany, train_mean_y.loc[commonCompany].values[:,0])
plt.xlabel('Airport_Company')
plt.ylabel('Delay_probability')
plt.title('Airline_Company and Delay Relation')
plt.show()

# =============================================================================

def arr_time(x):
    if x == '0600-0659' or x == '0700-0759' or x == '0800-0859' or x == '0900-0959' or x == '1000-1059' or x == '1100-1159' :
        return 'Morning'
    elif x == '1200-1259' or x == '1300-1359' or x == '1400-1459' or x == '1500-1559' or x == '1600-1659' or x == '1700-1759':
        return 'Evening'
    elif x == '1800-1859' or x == '1900-1959' or x == '2000-2059' or x == '2100-2159' or x == '2200-2259' or x == '2300-2359':
        return 'Night'
    else:
        return 'Early_Morning'
    
data['Big_Time_Block'] = data['ArrTimeBlk'].apply(lambda x :arr_time(x))

timeBlock = data['Big_Time_Block'].value_counts().index
train_group = data.groupby('Big_Time_Block')

train_mean_y = train_group['ArrDel15'].agg([lambda x:np.mean(x)])

fig, ax = plt.subplots(figsize = (15,8))
sns.barplot(timeBlock, train_mean_y.loc[timeBlock].values[:,0])
plt.xlabel('Big_Time_Block',fontsize=20)
plt.ylabel('Delay Probability',fontsize=20)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.title('Big_Time_Block and Delay Relation',fontsize=20)
plt.show()

# =============================================================================

commonNoon = data['ArrTimeBlk'].value_counts().index
train_group = data.groupby('ArrTimeBlk')

train_mean_y = train_group['ArrDel15'].agg([lambda x:np.mean(x)])

fig, ax = plt.subplots(figsize = (20, 8)) 
sns.barplot(commonNoon, train_mean_y.loc[commonNoon].values[:,0])
plt.xlabel('TimeBlock')
plt.ylabel('Delay_probability')
plt.title('TimeBlock and Delay Relation')
plt.show()

# =============================================================================

def awnd(x):
    if True:
        return str(x).split('.')[0]

data['AVERAGE_WIND'] = data['AWND'].apply(lambda x :awnd(x))

# average_wind = data['AVERAGE_WIND'].value_counts().index


train_group = data.groupby('AVERAGE_WIND')

train_mean_y = train_group['ArrDel15'].agg([lambda x:np.mean(x)]).rename(columns = {'<lambda>':'delay_freq'})

fig, ax = plt.subplots(figsize = (40,15))
sns.barplot([int(it) for it in train_mean_y.index], train_mean_y.values[:,0])
plt.xlabel('AVERAGE_WIND',fontsize=30)
plt.ylabel('Delay Probability',fontsize=30)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.title('AVERAGE_WIND and Delay Relation',fontsize=30)
plt.show()

# 查看離群值
# https://ithelp.ithome.com.tw/m/articles/10278000
# plt.figure(figsize=(2,5))
# plt.boxplot(data['AWND'],showmeans=True)
# plt.title('AWND')
# plt.show()

# =============================================================================

def prcp(x):
    if True:
        return str(x).split('.')[0]

data['prcp'] = data['PRCP'].apply(lambda x :awnd(x))

# average_wind = data['prcp'].value_counts().index

train_group = data.groupby('prcp')

train_mean_y = train_group['ArrDel15'].agg([lambda x:np.mean(x)]).rename(columns = {'<lambda>':'delay_freq'})

fig, ax = plt.subplots(figsize = (40,15))
sns.barplot([int(it) for it in train_mean_y.index], train_mean_y.values[:,0])
plt.xlabel('PRCP',fontsize=30)
plt.ylabel('Delay Probability',fontsize=30)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.title('PRCP and Delay Relation',fontsize=30)
plt.show()

# =============================================================================

def WSF2(x):
    if True:
        return str(x).split('.')[0]

data['wsf2'] = data['WSF2'].apply(lambda x :WSF2(x))

# average_wind = data['wsf2'].value_counts().index

train_group = data.groupby('wsf2')

train_mean_y = train_group['ArrDel15'].agg([lambda x:np.mean(x)]).rename(columns = {'<lambda>':'delay_freq'})

fig, ax = plt.subplots(figsize = (40,15))
sns.barplot([int(it) for it in train_mean_y.index], train_mean_y.values[:,0])
plt.xlabel('WSF2',fontsize=30)
plt.ylabel('Delay Probability',fontsize=30)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.title('WSF2 and Delay Relation',fontsize=30)
plt.show()

# =============================================================================

def WSF5(x):
    if True:
        return str(x).split('.')[0]

data['wsf5'] = data['WSF5'].apply(lambda x :WSF2(x))

average_wind = data['wsf5'].value_counts().index

train_group = data.groupby('wsf5')

train_mean_y = train_group['ArrDel15'].agg([lambda x:np.mean(x)]).rename(columns = {'<lambda>':'delay_freq'})

fig, ax = plt.subplots(figsize = (50,25))
sns.barplot([int(it) for it in train_mean_y.index], train_mean_y.values[:,0])
plt.xlabel('WSF5',fontsize=30)
plt.ylabel('Delay_probability',fontsize=30)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.title('WSF5 and Delay Relation',fontsize=30)
plt.show()

# =============================================================================

def snow(x):
    if True:
        return str(x).split('.')[0]

data['snow'] = data['SNOW'].apply(lambda x :snow(x))
# snow = data['snow'].value_counts().index

train_group = data.groupby('snow')

train_mean_y = train_group['ArrDel15'].agg([lambda x:np.mean(x)]).rename(columns = {'<lambda>':'delay_freq'})

fig, ax = plt.subplots(figsize = (30,15))
sns.barplot([int(it) for it in train_mean_y.index], train_mean_y.values[:,0])
plt.xlabel('SNOW',fontsize=30)
plt.ylabel('Delay Probability',fontsize=30)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.title('SNOW and Delay Relation',fontsize=30)
plt.show()

# =============================================================================

def TMAX(x):
    if True:
        return str(x).split('.')[0]

data['tmax'] = data['TMAX'].apply(lambda x :TMAX(x))
# snow = data['snow'].value_counts().index

train_group = data.groupby('tmax')

train_mean_y = train_group['ArrDel15'].agg([lambda x:np.mean(x)]).rename(columns = {'<lambda>':'delay_freq'})

fig, ax = plt.subplots(figsize = (30,15))
sns.barplot([int(it) for it in train_mean_y.index], train_mean_y.values[:,0])
plt.xlabel('TMAX',fontsize=30)
plt.ylabel('Delay Probability',fontsize=30)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.title('TMAX and Delay Relation',fontsize=30)
plt.show()

# =============================================================================

aircraft_type = data['Type Aircraft'].value_counts()
aircraft_counts = aircraft_type / aircraft_type.sum()
commonAircraft = aircraft_counts.iloc[:20].index
train_group = data.groupby('Type Aircraft')

train_mean_y = train_group['ArrDel15'].agg([lambda x:np.mean(x)])

fig, ax = plt.subplots(figsize = (12, 8)) 
sns.barplot(commonAircraft, train_mean_y.loc[commonAircraft].values[:,0])
plt.xlabel('Aircraft_Type',fontsize=18)
plt.ylabel('Delay Probability',fontsize=18)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.title('Aircraft_Type and Delay Relation',fontsize=18)
plt.show()

# =============================================================================

# 型號和delay之間影響關係
model_counts = data['Model'].value_counts()
model_freq = model_counts / sum(model_counts)
# 點進去看會發現 他會按照順序
commonModel = model_freq.iloc[:20].index

train_group = data.groupby('Model')
train_mean_y = train_group['ArrDel15'].agg([lambda x:np.mean(x)])

fig, ax = plt.subplots(figsize = (40,15))
sns.barplot(commonModel, train_mean_y.loc[commonModel].values[:,0])
plt.xlabel('model')
plt.ylabel('Delay Probability')
plt.xticks(rotation = 60)
plt.title('model and Delay Relation')
plt.show()

# =============================================================================

# 季和delay的關係
quarter = data['Quarter'].value_counts().index
train_group = data.groupby('Quarter')
train_mean_y = train_group['ArrDel15'].agg([lambda x:np.mean(x)])

fig, ax = plt.subplots(figsize = (25,15))
sns.barplot(quarter, train_mean_y.loc[quarter].values[:,0])
plt.xlabel('Quarter',fontsize=40)
plt.ylabel('Delay Probability',fontsize=40)
plt.xticks(fontsize=30)
plt.yticks(fontsize=25)
plt.title('Quarter and Delay Relation',fontsize=40)
plt.show()

# =============================================================================

wtxx = data['WT01'].value_counts().index
train_group = data.groupby('WT01')
train_mean_y = train_group['ArrDel15'].agg([lambda x:np.mean(x)*100])

fig, ax = plt.subplots(figsize = (25,15))
sns.barplot(wtxx, train_mean_y.loc[wtxx].values[:,0])
plt.xlabel('WT01',fontsize=40)
plt.ylabel('Delay Probability(%)',fontsize=40)
plt.xticks(fontsize=30)
plt.yticks(fontsize=25)
plt.title('WT01 and Delay Relation',fontsize=40)
plt.show()


# =============================================================================

wtxx = data['WT02'].value_counts().index
train_group = data.groupby('WT02')
train_mean_y = train_group['ArrDel15'].agg([lambda x:np.mean(x)*100])

fig, ax = plt.subplots(figsize = (25,15))
sns.barplot(wtxx, train_mean_y.loc[wtxx].values[:,0])
plt.xlabel('WT02',fontsize=40)
plt.ylabel('Delay Probability(%)',fontsize=40)
plt.xticks(fontsize=30)
plt.yticks(fontsize=25)
plt.title('WT02 and Delay Relation',fontsize=40)
plt.show()

# =============================================================================

wtxx = data['WT03'].value_counts().index
train_group = data.groupby('WT03')
train_mean_y = train_group['ArrDel15'].agg([lambda x:np.mean(x)*100])

fig, ax = plt.subplots(figsize = (25,15))
sns.barplot(wtxx, train_mean_y.loc[wtxx].values[:,0])
plt.xlabel('WT03',fontsize=40)
plt.ylabel('Delay Probability(%)',fontsize=40)
plt.xticks(fontsize=30)
plt.yticks(fontsize=25)
plt.title('WT03 and Delay Relation',fontsize=40)
plt.show()

# =============================================================================

wtxx = data['WT04'].value_counts().index
train_group = data.groupby('WT04')
train_mean_y = train_group['ArrDel15'].agg([lambda x:np.mean(x)*100])

fig, ax = plt.subplots(figsize = (25,15))
sns.barplot(wtxx, train_mean_y.loc[wtxx].values[:,0])
plt.xlabel('WT04',fontsize=40)
plt.ylabel('Delay Probability(%)',fontsize=40)
plt.xticks(fontsize=30)
plt.yticks(fontsize=25)
plt.title('WT04 and Delay Relation',fontsize=40)
plt.show()

# =============================================================================

wtxx = data['WT05'].value_counts().index
train_group = data.groupby('WT05')
train_mean_y = train_group['ArrDel15'].agg([lambda x:np.mean(x)*100])

fig, ax = plt.subplots(figsize = (25,15))
sns.barplot(wtxx, train_mean_y.loc[wtxx].values[:,0])
plt.xlabel('WT05',fontsize=40)
plt.ylabel('Delay Probability(%)',fontsize=40)
plt.xticks(fontsize=30)
plt.yticks(fontsize=25)
plt.title('WT05 and Delay Relation',fontsize=40)
plt.show()

# =============================================================================

wtxx = data['WT06'].value_counts().index
train_group = data.groupby('WT06')
train_mean_y = train_group['ArrDel15'].agg([lambda x:np.mean(x)*100])

fig, ax = plt.subplots(figsize = (25,15))
sns.barplot(wtxx, train_mean_y.loc[wtxx].values[:,0])
plt.xlabel('WT06',fontsize=40)
plt.ylabel('Delay Probability(%)',fontsize=40)
plt.xticks(fontsize=30)
plt.yticks(fontsize=25)
plt.title('WT06 and Delay Relation',fontsize=40)
plt.show()

# =============================================================================

wtxx = data['WT07'].value_counts().index
train_group = data.groupby('WT07')
train_mean_y = train_group['ArrDel15'].agg([lambda x:np.mean(x)*100])

fig, ax = plt.subplots(figsize = (25,15))
sns.barplot(wtxx, train_mean_y.loc[wtxx].values[:,0])
plt.xlabel('WT07',fontsize=40)
plt.ylabel('Delay Probability(%)',fontsize=40)
plt.xticks(fontsize=30)
plt.yticks(fontsize=25)
plt.title('WT07 and Delay Relation',fontsize=40)
plt.show()

# =============================================================================

wtxx = data['WT08'].value_counts().index
train_group = data.groupby('WT08')
train_mean_y = train_group['ArrDel15'].agg([lambda x:np.mean(x)*100])

fig, ax = plt.subplots(figsize = (25,15))
sns.barplot(wtxx, train_mean_y.loc[wtxx].values[:,0])
plt.xlabel('WT08',fontsize=40)
plt.ylabel('Delay Probability(%)',fontsize=40)
plt.xticks(fontsize=30)
plt.yticks(fontsize=25)
plt.title('WT08 and Delay Relation',fontsize=40)
plt.show()

# =============================================================================

wtxx = data['WT09'].value_counts().index
train_group = data.groupby('WT09')
train_mean_y = train_group['ArrDel15'].agg([lambda x:np.mean(x)*100])

fig, ax = plt.subplots(figsize = (25,15))
sns.barplot(wtxx, train_mean_y.loc[wtxx].values[:,0])
plt.xlabel('WT09',fontsize=40)
plt.ylabel('Delay Probability(%)',fontsize=40)
plt.xticks(fontsize=30)
plt.yticks(fontsize=25)
plt.title('WT09 and Delay Relation',fontsize=40)
plt.show()

# =============================================================================

wtxx = data['WT10'].value_counts().index
train_group = data.groupby('WT10')
train_mean_y = train_group['ArrDel15'].agg([lambda x:np.mean(x)*100])

fig, ax = plt.subplots(figsize = (25,15))
sns.barplot(wtxx, train_mean_y.loc[wtxx].values[:,0])
plt.xlabel('WT10',fontsize=40)
plt.ylabel('Delay Probability(%)',fontsize=40)
plt.xticks(fontsize=30)
plt.yticks(fontsize=25)
plt.title('WT10 and Delay Relation',fontsize=40)
plt.show()

# =============================================================================

wtxx = data['WT11'].value_counts().index
train_group = data.groupby('WT11')
train_mean_y = train_group['ArrDel15'].agg([lambda x:np.mean(x)*100])

fig, ax = plt.subplots(figsize = (25,15))
sns.barplot(wtxx, train_mean_y.loc[wtxx].values[:,0])
plt.xlabel('WT11',fontsize=40)
plt.ylabel('Delay Probability(%)',fontsize=40)
plt.xticks(fontsize=30)
plt.yticks(fontsize=25)
plt.title('WT11 and Delay Relation',fontsize=40)
plt.show()

# =============================================================================

wtxx = data['WT18'].value_counts().index
train_group = data.groupby('WT18')
train_mean_y = train_group['ArrDel15'].agg([lambda x:np.mean(x)*100])

fig, ax = plt.subplots(figsize = (25,15))
sns.barplot(wtxx, train_mean_y.loc[wtxx].values[:,0])
plt.xlabel('WT18',fontsize=40)
plt.ylabel('Delay Probability(%)',fontsize=40)
plt.xticks(fontsize=30)
plt.yticks(fontsize=25)
plt.title('WT18 and Delay Relation',fontsize=40)
plt.show()



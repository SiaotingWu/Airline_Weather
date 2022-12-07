# -*- coding: utf-8 -*-
"""
Created on Fri Oct  7 12:54:21 2022

@author: User
"""

import pandas as pd
import pyarrow as py
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import Normalize
from numpy.random import rand
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"
import seaborn as sns
import math
import matplotlib.ticker as mticker

data = pd.read_parquet('airline_weather_concat_1019')

###觀察前500筆
tmp = data.head(500)

# ==================================================================================
# 補充:
# plot color變化參考資料:https://matplotlib.org/stable/tutorials/colors/colormaps.html
# ==================================================================================

# 0. 觀察機場班機
Airport = data['Origin'].value_counts()







# 1. 航班出發和抵達的延遲，是否集中在某一時段或某些特定機場?
## 1.1 取前10名最會delay出發機場
Dep_Airport = data[data['DepartureDelayGroups'] > 0].value_counts('Origin')/data['Origin'].value_counts()            *100
### 畫圖
norm = plt.Normalize(Dep_Airport.min(), Dep_Airport.max())
norm_y = norm(Dep_Airport)
# map_vir = cm.get_cmap(name='plasma')
# color = map_vir(norm_y)
# Dep_Airport.nlargest(20).plot(kind='bar', stacked=True, color=color)
Dep_Airport.nlargest(20).plot(kind='bar', color = sns.color_palette('OrRd_r',20))
plt.title('20th The Most Delay\'s Airport(Origin)')
plt.xlabel('Origin Airport') # 增加x軸標籤
plt.ylabel('Delay Probability(%)') # 增加y軸標籤






## 1.2 取前20名最會delay抵達機場
Arr_Airport = data[data['ArrivalDelayGroups'] > 0].value_counts('Dest')/data['Dest'].value_counts()*100
### 畫圖2
fig, ax = plt.subplots(figsize = (20,10))
sns.Arr_Airport.nlargest(20).barplot()
plt.xlabel('Airplan\'s Age',fontsize=30)
plt.ylabel('Delay Probability(%)',fontsize=30)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.title('Airplane\'s Age and Delay Relation',fontsize=30)
plt.show()

### 畫圖
Arr_Airport.nlargest(20).plot(kind='bar',color=sns.color_palette('Greens_r',20))
plt.title('20th The Most Delay\'s Airport(Arrival)')
plt.xlabel('Dest Airport') # 增加x軸標籤
plt.ylabel('Delay Probability(%)') # 增加y軸標籤



## 1.3 航班出發Delay集中在某一時段
# 先區分成六個時段
# CRSDepTime 0001~0300, 0301~0600, 0601~0900, 0901~1200, 1201~1500, 1501~1800, 1801~2100, 2101~2400
#data.insert(11, 'CRSDT_Group', '0')
def CRSDT_Group(x):
    if x >= 1 and x <= 300:
        return '0001~0300';
    elif x >= 301 and x <= 600:
        return '0301~0600';    
    elif x >= 601 and x <= 900:
        return '0601~0900'
    elif x >= 901 and x <= 1200:
        return '0901~1200'
    elif x >= 1201 and x <= 1500:
        return '1201~1500'
    elif x >= 1501 and x <= 1800:
        return '1501~1800'
    elif x >= 1801 and x <= 2100:
        return '1801~2100'
    elif x >= 2101 and x <= 2400:
        return '2101~2400'

data['Dep_Time'] = data['CRSDepTime'].apply(lambda x:CRSDT_Group(x))
Dep_time = data[data['DepartureDelayGroups'] > 0].value_counts('Dep_Time')/data['Dep_Time'].value_counts() 
### 畫圖
Dep_time.plot(kind='bar')
plt.title('DepDelay v.s. Time')
plt.xlabel('Time') # 增加x軸標籤
plt.ylabel('DepDelay') # 增加y軸標籤

## 1.4 航班到達Delay集中在某一時段
data['Arr_Time'] = data['CRSArrTime'].apply(lambda x:CRSDT_Group(x))
Arr_time = data[data['ArrivalDelayGroups'] > 0].value_counts('Arr_Time')/data['Arr_Time'].value_counts() 
### 畫圖
Arr_time.plot(kind='bar')
plt.title('ArrDelay v.s. Time')
plt.xlabel('Time') # 增加x軸標籤
plt.ylabel('ArrDelay') # 增加y軸標籤


# 2. 誤點是否與星期幾(day_of_week)或每月幾號(day_of_month)有關?
## 2.1
day_of_week =  data[data['ArrivalDelayGroups'] > 0].value_counts('DayOfWeek')/data['DayOfWeek'].value_counts() *100
### 畫圖
day_of_week.plot(kind='bar', color = sns.color_palette('husl'))
plt.title('Day_of_Week and Delay Relation')
plt.xlabel('Day 0f Week') # 增加x軸標籤
plt.ylabel('Delay Probability(%)') # 增加y軸標籤

## 2.2
day_of_month =  data[data['ArrivalDelayGroups'] > 0].value_counts('DayofMonth')/data['DayofMonth'].value_counts() *100
### 畫圖
day_of_month.plot(kind='bar',color = sns.color_palette('viridis',31))
plt.title('Day_of_Month and Delay Relation')
plt.xlabel('Day of Month') # 增加x軸標籤
plt.ylabel('Delay Probability(%)') # 增加y軸標籤


# 3. 誤點原因是否為離場時間延遲(DEP_TIME_BLK)[誤點班機中起飛也誤點數量(1378/1764)]?
mask1 = data['ArrDel15'] > 0
mask2 = data['DepDel15'] > 0
DepTimeToDelay = (mask1 & mask2).sum()/mask1.sum()
# 77.17%

# 4. 大部分誤點的發生在上午還是下午? -> 先改為早上/下午/晚上/凌晨
def Time_Block(x):
    if x >= 1 and x <= 600:
        return 'After midnight';    
    elif x >= 601 and x <= 1200:
        return 'Moring'
    elif x >= 1201 and x <= 1800:
        return 'Afternoon'
    elif x >= 1801 and x <= 2400:
        return 'Night'

data['Arr_Time4'] = data['CRSArrTime'].apply(lambda x:Time_Block(x))
Arr_time4 = data[data['ArrDel15'] > 0].value_counts('Arr_Time4')/data['Arr_Time4'].value_counts() 
### 畫圖
Arr_time4.plot(kind='bar')
labels = ['After midnight','Moring','Afternoon','Night']
plt.title('ArrDelay v.s. Time_Block')
plt.xlabel('Time_Block') # 增加x軸標籤
plt.ylabel('ArrDelay') # 增加y軸標籤

# 5. 針對起飛機場，誤點次數及比率最高的機場?
## 5.1 起飛機場誤點次數最高的機場
DepAirport_max10_count = data[data['DepDel15'] > 0].value_counts('Origin')           
### 畫圖
DepAirport_max10_count.nlargest(10).plot(kind='bar')
plt.title('10th DepDelay\'s Airport(counts)')
plt.xlabel('Origin Airport') # 增加x軸標籤
plt.ylabel('DepDelay') # 增加y軸標籤
## 5.2 起飛機場誤點比率最高的機場
DepAirport_max10_persen = data[data['DepDel15'] > 0].value_counts('Origin')/data['Origin'].value_counts()            
### 畫圖
DepAirport_max10_persen.nlargest(10).plot(kind='bar')
plt.title('10th DepDelay\'s Airport(%)')
plt.xlabel('Origin Airport') # 增加x軸標籤
plt.ylabel('DepDelay') # 增加y軸標籤

# 6. 哪間航空公司最容易誤點?誤點的原因？
## 6.1 哪間航空公司起飛時最容易誤點
Airline_Dep = data[data['DepDel15'] > 0].value_counts('IATA_Code_Marketing_Airline')/data['IATA_Code_Marketing_Airline'].value_counts()*100
### 畫圖
Airline_Dep.plot(kind='bar',color = ['salmon', 'sandybrown', 'darkkhaki', 'limegreen', 'mediumseagreen', 'teal', 'skyblue', 'royalblue', 'mediumpurple', 'plum', 'violet'])
plt.title('Airline and Delay Relation')
plt.xlabel('Airline')
plt.ylabel('Delay Probability(%)')


## 6.2 哪間航空公司抵達時最容易誤點
Airline_Arr = data[data['ArrDel15'] > 0].value_counts('IATA_Code_Marketing_Airline')/data['IATA_Code_Marketing_Airline'].value_counts()*100
### 畫圖
Airline_Arr.plot(kind='bar',color = ['salmon', 'sandybrown', 'darkkhaki', 'limegreen', 'mediumseagreen', 'teal', 'skyblue', 'royalblue', 'mediumpurple', 'plum', 'violet'])
plt.title('Airline and Delay Relation')
plt.xlabel('Airline')
plt.ylabel('Delay Probability(%)')

## 6.3 各航班公司誤點原因
def Carrier(x):
    if x >0:
        return 1
    else:
        return 0
data['Carrier'] = data['CarrierDelay'].apply(lambda x:Carrier(x))
def Weather(x):
    if x >0:
        return 1
    else:
        return 0
data['Weather'] = data['WeatherDelay'].apply(lambda x:Weather(x))
def NAS(x):
    if x >0:
        return 1
    else:
        return 0
data['NAS'] = data['NASDelay'].apply(lambda x:NAS(x))
def Security(x):
    if x >0:
        return 1
    else:
        return 0
data['Security'] = data['SecurityDelay'].apply(lambda x:Security(x))

def LateAircraft(x):
    if x >0:
        return 1
    else:
        return 0
data['LateAircraft'] = data['LateAircraftDelay'].apply(lambda x:LateAircraft(x))

NoDelay = data['LateAircraftDelay'].isnull().value_counts()[1]

# Airline_reason = data[['IATA_Code_Marketing_Airline','Carrier','Weather','NAS','Security']].groupby('IATA_Code_Marketing_Airline').sum()
numCarrier = math.log(data['Carrier'].value_counts()[1],2)
numWeather = math.log(data['Weather'].value_counts()[1],2)
numNAS = math.log(data['NAS'].value_counts()[1],2)
numSecurity = math.log(data['Security'].value_counts()[1],2)
numLateAircraft = math.log(data['LateAircraft'].value_counts()[1])
numNoDelay = math.log(NoDelay,2)

delay_reason = ['CarrierDelay','WeatherDelay','NASDelay','SecurityDelay','LateAircraft','NoDelay']
delay_reason_times = [numCarrier,numWeather,numNAS,numSecurity,numLateAircraft,numNoDelay]


### 畫圖
fig, ax = plt.subplots(figsize=(12, 8)) 
sns.barplot(delay_reason, delay_reason_times)
plt.xlabel('Delay_Reason')
plt.ylabel('log(Delay_Times)')
plt.title('Delay_Reason and Times')
plt.show()


## 6.3 各航班公司誤點原因
def Carrier(x):
    if x >0:
        return 1
    else:
        return 0
data['Carrier'] = data['CarrierDelay'].apply(lambda x:Carrier(x))
def Weather(x):
    if x >0:
        return 1
    else:
        return 0
data['Weather'] = data['WeatherDelay'].apply(lambda x:Weather(x))
def NAS(x):
    if x >0:
        return 1
    else:
        return 0
data['NAS'] = data['NASDelay'].apply(lambda x:NAS(x))
def Security(x):
    if x >0:
        return 1
    else:
        return 0
data['Security'] = data['SecurityDelay'].apply(lambda x:Security(x))
def LateAircraft(x):
    if x >0:
        return 1
    else:
        return 0
data['LateAircraft'] = data['LateAircraftDelay'].apply(lambda x:LateAircraft(x))

NoDelay = data['LateAircraftDelay'].isnull().value_counts()[1]

Airline_reason = data[['IATA_Code_Marketing_Airline','Carrier','Weather','NAS','Security']].groupby('IATA_Code_Marketing_Airline').sum()

### Table
Airline_reason_table = pd.pivot_table(data, values=['Carrier','Weather','NAS','Security'], index=['IATA_Code_Marketing_Airline'],
                    aggfunc={'Carrier': np.mean,
                             'Weather': np.mean,
                             'NAS' : np.mean,
                             'Security' : np.mean})
### 畫圖
Airline_reason_table.plot.bar(rot=0)


## 6.3 各航班公司誤點原因
def Carrier(x):
    if x >0:
        return 1
    else:
        return 0
data['Carrier'] = data['CarrierDelay'].apply(lambda x:Carrier(x))

def Weather(x):
    if x >0:
        return 1
    else:
        return 0
data['Weather'] = data['WeatherDelay'].apply(lambda x:Weather(x))

def NAS(x):
    if x >0:
        return 1
    else:
        return 0
data['NAS'] = data['NASDelay'].apply(lambda x:NAS(x))

def Security(x):
    if x >0:
        return 1
    else:
        return 0
data['Security'] = data['SecurityDelay'].apply(lambda x:Security(x))

def LateAircraft(x):
    if x >0:
        return 1
    else:
        return 0
data['LateAircraft'] = data['LateAircraftDelay'].apply(lambda x:LateAircraft(x))

NoDelay = data['LateAircraftDelay'].isnull().value_counts()[1]

# Airline_reason = data[['IATA_Code_Marketing_Airline','Carrier','Weather','NAS','Security']].groupby('IATA_Code_Marketing_Airline').sum()
numCarrier = data['Carrier'].value_counts()[1]
numWeather = data['Weather'].value_counts()[1]
numNAS = data['NAS'].value_counts()[1]
numSecurity = data['Security'].value_counts()[1]
numLateAircraft = data['LateAircraft'].value_counts()[1]
numNoDelay = NoDelay

delay_reason = ['CarrierDelay','WeatherDelay','NASDelay','SecurityDelay','LateAircraft','NoDelay']
delay_reason_times = [numCarrier,numWeather,numNAS,numSecurity,numLateAircraft,numNoDelay]


### 畫圖
fig, ax = plt.subplots(figsize=(12, 8)) 
sns.barplot(delay_reason, delay_reason_times)
plt.xlabel('Delay_Reason')
plt.ylabel('log(Delay_Times)')
plt.title('Delay_Reason and Times')
plt.show()


# 7. 誤點的原因？
## 7.1 哪間航空公司起飛時最容易誤點
Airline_Dep = data[data['DepDel15'] > 0].value_counts('IATA_Code_Marketing_Airline')/data['IATA_Code_Marketing_Airline'].value_counts()
### 畫圖
Airline_Dep.plot.bar()
plt.title('DepDelay v.s. Airline')
plt.xlabel('Airline')
plt.ylabel('DepDelay(%)')

# 先取市占率 去看哪些值是我們值得看的
Company_counts = data['IATA_Code_Marketing_Airline'].value_counts()
Company_counts = Company_counts / Company_counts.sum()
commonCompany = Company_counts.index

# 依照 IATA 去分組
train_group = data.groupby('IATA_Code_Marketing_Airline')

# 把分組結果依照 ArrDel15 去
train_mean_y = train_group['ArrDel15'].agg([lambda x:np.mean(x)])*100

fig, ax = plt.subplots(figsize = (12, 8)) 
sns.barplot(commonCompany, train_mean_y.loc[commonCompany].values[:,0])
plt.xlabel('Airport_Company',fontsize=20)
plt.ylabel('Delay_probability(%)',fontsize=20)
plt.title('Airline_Company and Delay Relation',fontsize=20)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.show()



# 8. 分年份
## 2018
data_2018 = data[data['Year']==2018]
numORD = data_2018['Origin']=='ORD'.value_counts()[1]
numATL = data_2018['Weather'].value_counts()[1]


Origin = ['ORD','ATL','DEN','DFW','CLT','LAX','SEA','IAH','PHX','LAS']
delay_reason_times = [numCarrier,numWeather,numNAS,numSecurity,numLateAircraft,numNoDelay]

fig, ax = plt.subplots(figsize=(12, 8)) 
sns.barplot()
plt.xlabel('Origin Airport')
plt.ylabel('Counts')
plt.title('Top10 Flight Airports in 2018(Origin)')
plt.show()
Dest_2018 = data.value_counts('Dest')

## 2019

## 2020

## 2021




# 8. 溫度和delay之間影響關係
## MinTemp
def TMin(x):
    if True:
        return str(x).split('.')[0]

data['TMin'] = data['TMIN'].apply(lambda x :TMin(x))
# snow = data['snow'].value_counts().index

train_group = data.groupby('TMin')

train_mean_y = train_group['ArrDel15'].agg([lambda x:np.mean(x)]).rename(columns = {'<lambda>':'delay_freq'})*100

fig, ax = plt.subplots(figsize = (30,7))
sns.barplot([int(it) for it in train_mean_y.index], train_mean_y.values[:,0])
plt.xlabel('Min Temp(℉)',fontsize=30)
plt.ylabel('Delay Probability(%)',fontsize=30)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
tick_spacing = train_mean_y.index.size/71 # x軸密集度
ax.xaxis.set_major_locator(mticker.MultipleLocator(tick_spacing))
plt.title('MinTemp and Delay Relation',fontsize=30)
plt.show()

## MaxTemp
### 先換算成攝氏
def TMax(x):
    if True:
        return (x-32)*5/9
data['tmax']=data['TMAX'].apply(lambda x :TMax(x))

def tmax(x):
    if True:
        return str(x).split('.')[0]

data['TMax'] = data['tmax'].apply(lambda x :tmax(x))

train_group = data.groupby('TMax')

train_mean_y = train_group['ArrDel15'].agg([lambda x:np.mean(x)]).rename(columns = {'<lambda>':'delay_freq'})*100

fig, ax = plt.subplots(figsize = (30,7))
sns.barplot([int(it) for it in train_mean_y.index], train_mean_y.values[:,0])
plt.xlabel('Max Temp(℃)',fontsize=30)
plt.ylabel('Delay Probability(%)',fontsize=30)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
tick_spacing = train_mean_y.index.size/29 # x軸密集度
ax.xaxis.set_major_locator(mticker.MultipleLocator(tick_spacing))
plt.title('MaxTemp and Delay Relation',fontsize=30)
plt.show()

# 9. 飛機年齡
data['age'] = data['Year']-data['MFR Year']
# snow = data['snow'].value_counts().index
data_age = data[data['age']>5]
train_group = data_age.groupby('age')

train_mean_y = train_group['ArrDel15'].agg([lambda x:np.mean(x)]).rename(columns = {'<lambda>':'delay_freq'})*100

fig, ax = plt.subplots(figsize = (30,10))
sns.barplot([int(it) for it in train_mean_y.index], train_mean_y.values[:,0])
plt.xlabel('Airplan\'s Age',fontsize=30)
plt.ylabel('Delay Probability(%)',fontsize=30)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.title('Airplane\'s Age and Delay Relation',fontsize=30)
plt.show()


# 10. 機型
aircraft_type = data['Type Aircraft'].value_counts()
aircraft_counts = aircraft_type / aircraft_type.sum()
commonAircraft = aircraft_counts.iloc[:20].index
train_group = data.groupby('Type Aircraft')

train_mean_y = train_group['ArrDel15'].agg([lambda x:np.mean(x)])*100

fig, ax = plt.subplots(figsize = (12, 9)) 
sns.barplot(commonAircraft, train_mean_y.loc[commonAircraft].values[:,0])
plt.xlabel('Aircraft_Type',fontsize=20)
plt.ylabel('Delay Probability(%)',fontsize=20)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.title('Aircraft_Type and Delay Relation',fontsize=18)
for x,y in zip(commonAircraft,train_mean_y.loc[commonAircraft].values[:,0]):
 plt.text(x, y+0.05, '%.0f' % y, ha='center', va= 'bottom',fontsize=11)
plt.show()

# 11. WT01~WT18
quarter = data['WT01'].value_counts().index
train_group = data.groupby('WT01')
train_mean_y = train_group['ArrDel15'].agg([lambda x:np.mean(x)])*100

fig, ax = plt.subplots(figsize = (25,15))
sns.barplot(quarter, train_mean_y.loc[quarter].values[:,0])
plt.xlabel('WT01',fontsize=40)
plt.ylabel('Delay Probability(%)',fontsize=40)
plt.xticks(fontsize=30)
plt.yticks(fontsize=25)
plt.title('WT01 and Delay Relation',fontsize=40)
plt.show()



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

train_mean_y = train_group['ArrDel15'].agg([lambda x:np.mean(x)])*100

fig, ax = plt.subplots(figsize = (15,8))
sns.barplot(timeBlock, train_mean_y.loc[timeBlock].values[:,0])
plt.xlabel('Big_Time_Block',fontsize=20)
plt.ylabel('Delay Probability(%)',fontsize=20)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.title('Big_Time_Block and Delay Relation',fontsize=20)
plt.show()

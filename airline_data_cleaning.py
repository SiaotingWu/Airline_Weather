# -*- coding: utf-8 -*-
"""
Created on Sun Oct 16 15:45:31 2022

@author: User
"""

import pandas as pd
import pyarrow as py

# 讀取airline_data
airline_data = pd.read_parquet('C:/Users/User/Desktop/Topic/爬蟲/.126/airline_data/new_airline_data')

airline_col = ['Year','Quarter','Month','DayofMonth','DayOfWeek',
               'FlightDate','IATA_Code_Marketing_Airline','Tail_Number',
               'Origin','Dest','CRSDepTime','DepTime','DepDelay','DepDelayMinutes',
               'DepDel15','DepartureDelayGroups','TaxiOut','WheelsOff','WheelsOn',
               'TaxiIn','CRSArrTime','ArrTime','ArrDelay','ArrDelayMinutes',
               'ArrDel15','ArrivalDelayGroups','Cancelled','CancellationCode',
               'Diverted','ActualElapsedTime','AirTime','Distance','CarrierDelay',
               'WeatherDelay','NASDelay','SecurityDelay','LateAircraftDelay',
               'DivAirportLandings']

airline_data = airline_data.loc[:,airline_col]


# 輸出篩選過後38個欄位的檔案
airline_data.to_parquet("airline_data_38")

# airline_info = airline_data.info()

# airline_head = airline_data.head(100)

# airline_nullsum = airline_data.isnull().sum()


# 讀取保留38欄位之data
airline_data = pd.read_parquet('C:/Users/User/Desktop/Topic/airline_data_38')


# 討論cancel班機要不要刪掉或保留與天氣有關之cancel班機
# 觀察cancell原因
cancel = airline_data[airline_data['Cancelled']==1]
cancel[''].value_counts()

# method1. 直接刪除所有cancel data(drop:707354筆, keep: 25826582筆)
airline_data_dropCancel = airline_data[~airline_data['Cancelled'].isin([1])]
# drop cancel相關欄位
airline_data_dropCancel.drop(columns=['Cancelled','CancellationCode'],inplace = True)

# 將準點airline的nan值轉為0
airline_data_dropCancel['CarrierDelay'].fillna(value=0,inplace=True)
airline_data_dropCancel['WeatherDelay'].fillna(value=0,inplace=True)
airline_data_dropCancel['NASDelay'].fillna(value=0,inplace=True)
airline_data_dropCancel['SecurityDelay'].fillna(value=0,inplace=True)
airline_data_dropCancel['LateAircraftDelay'].fillna(value=0,inplace=True)
# 取消的班機也會被編成0!!!!!!!FUCK 之前沒想到也沒注意到

# 輸出篩選過後36個欄位的檔案
airline_data_dropCancel.to_parquet("airline_data_cancel")

# 讀取保留36欄位之data
airline_data_dropCancel = pd.read_parquet('C:/Users/User/Desktop/Topic/airline_data_cancel')

# 觀察有空值欄位數量
airline_nullsum = airline_data_dropCancel.isnull().sum()


###### 處理有空值之欄位 ######
# 1. Drop DepTime & Tail_Number is Null

## 檢查
depNull = airline_data_dropCancel[airline_data_dropCancel['DepTime'].isnull()]

tailNull = airline_data_dropCancel[airline_data_dropCancel['Tail_Number'].isnull()]

## 刪除
airline_data_dropCancel.dropna(subset=['DepTime','Tail_Number'], inplace = True)


# 2. TaxiOut & TaxiIn => 空值填平均

# =============================================================================
# ## RUN 太久
# airline_TaxiOut = airline_data_dropCancel.apply(lambda x:x. fillna(airline_data_dropCancel.group('Origin').TaxiOut.mean()[x.Origin]), axis=1)
# 
# airline_TaxiOut = airline_data_dropCancel.apply(lambda x:x. fillna(airline_data_dropCancel.group('Origin').TaxiOut.mean()[x.Origin]), axis=1)
# 
# =============================================================================

### 利用 groupby & transform 填補
airline_data_dropCancel['TaxiOut'] = airline_data_dropCancel.groupby('Origin')[['TaxiOut']].transform(lambda x: x.fillna(x.mean()))

airline_data_dropCancel['TaxiIn'] = airline_data_dropCancel.groupby('Origin')[['TaxiIn']].transform(lambda x: x.fillna(x.mean()))

### 檢查空值填補後狀況
Origin_mask = airline_data[(airline_data['Origin'] == 'HNL')& (airline_data['TaxiOut'] % 1 != 0)]

# 輸出檔案
airline_data_dropCancel.to_parquet("airline_data_1005")
# 讀取檔案
airline_data_dropCancel = pd.read_parquet('C:/Users/User/Desktop/Topic/airline_data_1005')
# 各欄位空值總和
airline_data_nullsum = airline_data_dropCancel.isnull().sum()
# 重置數據幀索引的方法
airline_data_dropCancel.reset_index(drop=True, inplace = True)


# 3. 
# *****************Drop是欄位ArrDelay is Null***************** 
airline_data_dropCancel.dropna(subset=['ArrDelay','DepDelay','DivAirportLandings'], inplace = True)

# *********************刪除不需要使用之欄位**********************
airline_data_dropCancel.drop(['WheelsOff','WheelsOn','AirTime'], axis=1, inplace=True)
# 各欄位空值總和
airline_data_nullsum = airline_data_dropCancel.isnull().sum()
# 輸出檔案
airline_data_dropCancel.to_parquet('airline_final')
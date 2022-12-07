# -*- coding: utf-8 -*-
"""
Created on Sat Oct 29 15:35:39 2022

@author: User
"""

import pandas as pd
from glob import glob
import pymysql
a1=pd.read_csv('OTHER.csv')
a2=a1[['STATION','NAME','DATE','AWND','PRCP','TMAX','TMIN','WSF2','WSF5']]
#選取所要欄位
a2.isnull().sum()
#確認空值數量
a3=a2.fillna(a2.interpolate())
#填補空值(採上下兩值平均的方式去填補空值)
a3.isnull().sum()
#確認空值數量
a4=pd.read_csv('SNOW_WT.csv')
#讀取另一個資料
a5=a4[['NAME','DATE','SNOW','WT01','WT02','WT03','WT04','WT05','WT06','WT07','WT08','WT09','WT10','WT11','WT18']]
#選取所要欄位

#準備進行欄位合併
a3['new']=a3['DATE']+""+a3['NAME']
a5['new']=a5['DATE']+""+a5['NAME']
#新增特徵欄位

a3.to_csv('a1.csv')
a5.to_csv('a2.csv')
#先存檔

files = glob('a*.csv')
df_list = [pd.read_csv(file) for file in files]
result = pd.merge(df_list[0], df_list[1], on='new')
#讀取兩個檔案並將兩個檔案以新增加的new欄位進行合併
result.isnull().sum()
#這時檢查欄位會發現，因為原本的資料有一樣名稱的欄位，所以會以x跟y區分
result[['NAME','DATE']]=result[['NAME_x','DATE_x']]
#所以要另外新增欄位抓取原本的資料
a10=result[['STATION','NAME','DATE','AWND','PRCP','TMAX','TMIN','WSF2','WSF5','SNOW','WT01','WT02','WT03','WT04','WT05','WT06','WT07','WT08','WT09','WT10','WT11','WT18']]
#重新抓取需要的欄位資料 目前檔案數量為524859筆
a10.drop(a10.loc[(a10['NAME']=='LANAI AIRPORT 656, HI US') | (a10['NAME']=='DEVILS LAKE MUNICIPAL AIRPORT, ND US')| (a10['NAME']=='WILLISTON AIRPORT, ND US')| (a10['NAME']=='KAPALUA W. MAUI AIRPORT 462.4, HI US')| (a10['NAME']=='LAREDO INTERNATIONAL AIRPORT, TX US')| (a10['NAME']=='MARQUETTE WEATHER SERVICE OFFICE AIRPORT, MI US')].index, inplace=True)
#然後將不要的氣象站drop掉 drop之後剩下518353筆
a10.to_parquet('weather_data_1006')
#最後存檔~~

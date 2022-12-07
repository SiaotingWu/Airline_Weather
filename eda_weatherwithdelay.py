import pickle
import gzip
import pandas as pd
from sklearn import preprocessing
import sys
from sklearn.preprocessing import LabelEncoder
import sys

# 將所有航班資料載入
data = pd.read_parquet("C:/Users/User/Desktop/airline/airline_weather_concat_1025")
# 將出發與目的地所對應的數字，將其丟入到後面的資料去做對應
Dest_map = data['Dest'].value_counts().to_dict()
Origin_map = data['Origin'].value_counts().to_dict()

def predict_ans(file_name):
    modeldir = './model'
    
    # 將新的資料集 load 進來 
    data_pred = pd.read_parquet(f'C:/Users/User/Desktop/airline/{file_name}')
    # data_pred = pd.read_parquet(f'C:/Users/User/Desktop/airline/data_test')
    
    # 將 index 整理好
    data_pred.reset_index(drop=True,inplace=True)
    
    # 使用者匯入資料的時候，並不會有 "WTSUMx","WTSUMy" 這兩個特徵欄位，所以在這邊加入新特徵
    data_pred['WTSUMx'] = (data_pred['WT01_x']+data_pred['WT02_x']+data_pred['WT03_x']+data_pred['WT04_x']+
                           data_pred['WT05_x']+data_pred['WT06_x']+data_pred['WT07_x']+data_pred['WT08_x']+
                           data_pred['WT09_x']+data_pred['WT10_x']+data_pred['WT11_x']+data_pred['WT18_x'])
    
    data_pred['WTSUMy'] = (data_pred['WT01_y']+data_pred['WT02_y']+data_pred['WT03_y']+data_pred['WT04_y']+
                           data_pred['WT05_y']+data_pred['WT06_y']+data_pred['WT07_y']+data_pred['WT08_y']+
                           data_pred['WT09_y']+data_pred['WT10_y']+data_pred['WT11_y']+data_pred['WT18_y'])
    
    # 將資料做備份
    data_copy = data_pred.copy()
    
    # 把航空公司做特徵轉碼
    data_copy['IATA_Code_Marketing_Airline'] = LabelEncoder().fit_transform(data_copy['IATA_Code_Marketing_Airline'])

    # 將出發與抵達地的文字資料做對應
    data_copy['Dest'] = data_copy['Dest'].map(Dest_map)
    data_copy['Origin'] = data_copy['Origin'].map(Origin_map)
    
    # 選擇要使用的 col
    col_select =['Year', 'Quarter', 'Month', 'DayofMonth', 'DayOfWeek',
           'IATA_Code_Marketing_Airline', 'Origin', 'Dest', 'CRSDepTime',
           'CRSArrTime', 'DistanceGroup',
           
           'AWND_x', 'PRCP_x', 'TMAX_x', 'TMIN_x', 'WSF2_x',
           'WSF5_x', 'SNOW_x', 'WT01_x', 'WT02_x', 'WT03_x', 'WT04_x', 'WT05_x',
           'WT06_x', 'WT07_x', 'WT08_x', 'WT09_x', 'WT10_x', 'WT11_x', 'WT18_x',
           
           'AWND_y', 'PRCP_y', 'TMAX_y', 'TMIN_y', 'WSF2_y', 
           'WSF5_y', 'SNOW_y','WT01_y', 'WT02_y', 'WT03_y', 'WT04_y', 'WT05_y', 
           'WT06_y', 'WT07_y','WT08_y', 'WT09_y', 'WT10_y', 'WT11_y', 'WT18_y',
           
           'WTSUMx', 'WTSUMy']
    
    # 將選擇的特徵重新做一張表
    X = data_copy[col_select]
    
    #### NORMALIZE X ####
    # Normalize so everything is on the same scale. 
    cols = X.columns
    min_max_scaler = preprocessing.MinMaxScaler(feature_range=(-1,1))
    np_scaled = min_max_scaler.fit_transform(X)
    
    # new data frame with the new scaled data. 
    X = pd.DataFrame(np_scaled, columns = cols)
    
    
    # 讀取gzip.Model (模型匯入)
    with gzip.open(f'{modeldir}/grid.pgz', 'r') as xgbm2:
        xgb2 = pickle.load(xgbm2)
        # 新資料集匯入模型做預測
        pred = xgb2.predict(X)
        # 新資料的預測值，轉換為 dataframe
        df_pred = pd.DataFrame(pred)
        
        # # 年、月、日 做一些轉換
        # data_pred = data_pred[col_select]
        # data_pred['Year'] = data_pred['Year'].astype('str')
        # data_pred['Month'] = data_pred['Month'].astype('str')
        # data_pred['DayofMonth'] = data_pred['DayofMonth'].astype('str')

        # # Month、Day 前面補一個0，e.g. 1 --> 01，12 --> 012
        # data_pred['Month'] = '0' + data_pred['Month']
        # data_pred['DayofMonth'] = '0' + data_pred['DayofMonth']

        # # 再取數字的後兩位，即可達成  01、02、03、...、10、11、12
        # data_pred['Month'] = data_pred['Month'].str[-2:]
        # data_pred['DayofMonth'] = data_pred['DayofMonth'].str[-2:]

        # # 將 Year,Month,Day 合併成 DATE，格式為 2018-06-08
        # data_pred['DATE'] = data_pred['Year'] +'-'+ data_pred['Month'] + '-' + data_pred['DayofMonth'] 
        
        
        # # 把剛剛拆開來的資料，全部丟棄
        # data_pred.drop(columns=['Year','Month','DayofMonth'],inplace=True)
        
        # # 把新的日期欄位移動到最前面
        # cols = data_pred.columns.tolist()
        # cols.insert(0,cols.pop(cols.index('DATE')))
        # data_pred = data_pred[cols]
        
        # 將預測值跟使用者輸入的資料合併
        future_pred = pd.concat([data_pred, df_pred], axis = 1)

        # 匯出一個 新的檔案
        future_pred.to_csv('future_pred.csv')

# 在 CMD 上跑程式時，去抓第一個參數(檔名)，並丟進模型
file_name = sys.argv[1]
predict_ans(file_name)


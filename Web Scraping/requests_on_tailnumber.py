# 安裝相關跳套件
import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
import csv

# 匯入機尾資料，在jupyter notebook，用shape確認幾筆資料
numList=pd.read_csv("C:/Users/User/Desktop/tail_number1.txt",header=None)
numList.shape[0]

# 給網址
url="https://registry.faa.gov/aircraftinquiry/Search/NNumberResult"
headers = {
    "User-Agent":'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
}
# 先預設輸入參數
payload = {'NNumbertxt':''}

# 定義函數，以後抓取輸入參數
def get_tail(serial):
    payload['NNumbertxt']=serial
    return payload

# 用request.post方法抓取第一筆機尾資料
response = requests.post(url=url, headers=headers, data = get_tail(numList.iloc[0,0]))
soup = BeautifulSoup(response.text, 'html.parser')
td_content = soup.find_all(attrs={"data-label": True, "colspan":False})

# 機尾資料強制轉型成dataframe，否則無法存取編輯
td_df = pd.DataFrame(td_content)

# 用dataframe創造機尾號碼的欄位名稱及抓取第一筆資料的機尾號碼
# 抓取資料為str，用list1包裝起來並強制轉換成dataframe
tail_no_label = pd.DataFrame(['Tail Number'])
tail_no = numList.iloc[0,0]
tail_no = pd.DataFrame([tail_no])

# 因印出資料為一列的欄位名稱和欄位值，所以用iloc去抓取，
# 設定所有屬於欄位值為index1，欄位名稱為content1
index1 = td_df.iloc[0:len(td_df):2]
content1 = td_df.iloc[1:len(td_df):2]

# 並將機尾號碼跟及其欄位名稱與index1,content1合併
index1 = pd.concat([tail_no_label,index1],axis=0)
content1 = pd.concat([tail_no,content1],axis=0)

# 由於抓取出的資料dataframe有對應的key值，
# 用reset_index重置index，最後將兩個欄位合併concat起來，並列欄互換
# 在jupyter notebook，res_df可顯示第一筆資料內容
index1.reset_index(drop=True, inplace=True)
content1.reset_index(drop=True, inplace=True)
res_df=pd.concat([index1,content1],axis=1).T
res_df

# 用for迴圈將機尾資料總數重複執行(1,numList.shape[0])->跳過第一筆直到最後一筆
# 印出第幾筆和每一筆處理的機尾號碼，
# data呼叫get_tail函數並去抓取那個欄位名稱
# 找出機尾號碼相對應的資料並轉成dataframe，
# 因為已經有欄位名稱，這一次只取欄位值content1，並列欄互換
# concat到之前第一筆有欄位名稱的資料
# 迴圈執行完，輸出成csv並且不要有index,header
for i in range(1,numList.shape[0]):
    print(i+1, numList.iloc[i,0])
    response = requests.post(url=url, headers=headers ,data = get_tail(numList.iloc[i,0]))
    soup = BeautifulSoup(response.text, 'html.parser')
    content = soup.find_all(attrs={"data-label": True, "colspan":False})
    td_df = pd.DataFrame(content)
    content1 = td_df.iloc[1:len(td_df):2]
    content1.reset_index(drop=True, inplace=True)
    content1=content1.T
    res_df=pd.concat([res_df,content1])
    sleep(1)
res_df.to_csv("tail_no_detail.csv",header=False, index=False)

# 可以讀取csv，並檢查欄位數大小
a = pd.read_csv("tail_no_detail.csv")
a.shape[:]
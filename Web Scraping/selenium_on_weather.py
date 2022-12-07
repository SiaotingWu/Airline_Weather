# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 13:26:25 2022

@author: User
"""


from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep

# from data import airline_data
# place = airline_data['Dest'].unique().tolist()

place=[]
with open('place1.txt','r') as f:
    for line in f:
        place.append(line.strip('\n').split(',')[0])
# print(result)

def get_weather_date():
    # 這邊用 try 去包，是怕會出現錯誤
    try:
        # 加入購物車的時候，每次只能裝 100 筆資料，所以我在這邊切割每 100 比做一個切割。
        for n in range(0,301,100):
            url = "https://www.ncdc.noaa.gov/cdo-web/search"
            
            driver_path = "c:/Users/user/Desktop/chromedriver_win32/chromedriver.exe"
            driver = webdriver.Chrome(executable_path=driver_path) # Use Chrome
            sleep(3)    
            
            driver.get(url)
            sleep(3)    
            
            # 選擇資料類型 Select Weather Observation Type/Dataset
            s1 = Select(driver.find_element(By.ID, 'selectedDataset'))
            s1.select_by_index(1)
            sleep(1)
            
            # 選擇日期
            # 年
            s1 = driver.find_elements(By.CLASS_NAME, 'noaa-daterange-input')
            s1[0].click()
            sleep(1)
            
            s1 = Select(driver.find_element(By.CLASS_NAME, 'ui-datepicker-year'))
            s1.select_by_index(4)
            sleep(1)
            
            # 月/日
            s1 = driver.find_element(By.CLASS_NAME, 'ui-state-default')
            s1.click()
            sleep(1)
            
            s1 = driver.find_element(By.CLASS_NAME, 'noaa-daterange-btn.noaa-daterange-applybtn')
            s1.click()
            sleep(1)
            
            # 選擇機場地區，並送出請求
            s1 = driver.find_element(By.ID, 'selectedSearchString')
            s1.send_keys(place[0] + Keys.RETURN)
            
            # 進入新的網頁，休息5秒，等網頁跑完再繼續下去
            sleep(5)
            
            s1 = driver.find_elements(By.CLASS_NAME, 'button.cartButton')
            s1[0].click()
            sleep(1)
    
            # 選擇要的資料加入購物車，每 100 筆做一個循環
            for i in place[n:n+100]:
                print(place.index(i),i)
                
                # 定位搜尋欄位
                s1 = driver.find_element(By.ID, 'searchString')
                # 把搜尋欄位，前一個資料做清除
                s1.clear()
                sleep(2)
                print('1') # 這邊我只是在確認邏輯是否正確，我下的指令是否有照我的想法跑，後面的 print('2')3、4、5、6、7，這些都是
                # 把要搜尋的資料送進欄位裡面，並且同時案 enter
                s1.send_keys(i + Keys.RETURN)
                sleep(2)
                
                # 送進去的資料會跑出多筆，我要去查找哪個才是我想要的資料，所以我把他吐給我的資料全部定位抓下來，後面用邏輯去判斷
                place_list = driver.find_elements(By.CSS_SELECTOR, '.title a')
                print('2')
                
                
                # 92~117 行開始進行判斷，我要什麼樣的資料，才放入購物車
                # k,l 會這樣設定是因為我想要解決，當電腦吐給我的資料都是我不要的時候，我要想辦法把當成缺失值，放入我的 missing_data 的 list 裡面
                k = len(place_list)-1
                l = 0
                
                # 當發現沒有資料的時候，我就會直接進入到 else，如果有資料會進入到 if 裡面
                if place_list[1:]:
                    # 每次 check 一次欄位，發現不是我要的資料，我就將 l+1
                    for j in place_list[1:]:
                        print(j.text)
                        l += 1
                        print('3')
                        # 判斷此筆資料，裡面是否有 AIRPORT，這個文字
                        if 'AIRPORT' in j.text:
                            print('4')
                            # 108~110 如果我就將此筆資料放入購物車，在定位的時候需要判斷一下他在第幾個地方
                            s1 = driver.find_elements(By.CLASS_NAME, 'button.cartButton')
                            l = 2*(l-1)
                            s1[l].click()
                            sleep(1)
                            # 如果有資料我同時也會直接 break 把迴圈斷掉 
                            break
                        # 這邊就是當多筆資料都不是我想要的資料，我就會將此筆資料當作 missing_data，然後 append 到 list 裡面
                        if k == l:
                            missing_data.append(i)
                            print('5')
            
                else:
                    missing_data.append(i)
                    print('6')
                    
                    
                print('7')  
            
            # 這邊就是定位後續的資料
            s1 = driver.find_elements(By.CLASS_NAME, 'button.cartButton')
            s1[0].click()
            sleep(1)
            s1 = driver.find_elements(By.ID, 'widgetBodyInner')
            s1[0].click()
            sleep(1)
            
            # 進入新的網頁，休息5秒，等網頁跑完再繼續下去
            sleep(5)
            
            # 選擇 csv 檔，並送出請求
            s1 = driver.find_elements(By.ID, 'GHCND_CUSTOM_CSV')
            s1[0].click()
            sleep(1)
            
            s1 = driver.find_elements(By.CLASS_NAME, 'noaa-daterange-input')
            s1[0].click()
            sleep(1)
            
            s1 = Select(driver.find_element(By.CLASS_NAME, 'ui-datepicker-year'))
            s1.select_by_index(4)
            sleep(1)
            
            # 月/日
            s1 = driver.find_element(By.CLASS_NAME, 'ui-state-default')
            s1.click()
            sleep(1)
            
            s1 = driver.find_element(By.CLASS_NAME, 'noaa-daterange-btn.noaa-daterange-applybtn')
            s1.click()
            sleep(1)
            
            s1 = driver.find_elements(By.CLASS_NAME, 'floatRight')
            s1[0].click()
            
            # 進入新的網頁，休息5秒，等網頁跑完再繼續下去
            sleep(5)
            
            # 選擇還要新加入的資料 Select data types for custom output
            try:
                s1 = driver.find_elements(By.ID, 'PRCP')
                s1[0].click()
            except IndexError:
                pass
            
            try:
                s1 = driver.find_elements(By.ID, 'TEMP')
                s1[0].click()
            except IndexError:
                pass
            
            try:
                s1 = driver.find_elements(By.ID, 'WIND')
                s1[0].click()
            except IndexError:
                pass
            
            try:
                s1 = driver.find_elements(By.ID, 'LAND')
                s1[0].click()
            except IndexError:
                pass
            
            try:
                s1 = driver.find_elements(By.ID, 'WATER')
                s1[0].click()
            except IndexError:
                pass
            
            try:
                s1 = driver.find_elements(By.ID, 'SUN')
                s1[0].click()
            except IndexError:
                pass
            
            
            try:
                s1 = driver.find_elements(By.ID, 'WXTYPE')
                s1[0].click()
            except IndexError:
                pass
            
            try:
                s1 = driver.find_elements(By.ID, 'buttonContinue')
                s1[0].click()
            except IndexError:
                pass
                
            # 進入新的網頁，休息5秒，等網頁跑完再繼續下去
            sleep(5)
            
            # 填信箱
            s1 = driver.find_elements(By.CLASS_NAME, 'emailIcon')
            s1[0].send_keys('23139@cyvs.tyc.edu.tw')
            s1[1].send_keys('23139@cyvs.tyc.edu.tw')
            s1 = driver.find_elements(By.ID, 'buttonSubmit')
            s1[0].click()
            
            sleep(5)
            
            driver.close()
            
    except:
        driver.close()
    

# 創建一個 list 去包裝遺失資料(抓不到的資料)
missing_data = []
get_weather_date()
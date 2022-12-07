from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from time import sleep


url = "https://www.transtats.bts.gov/DL_SelectFields.aspx?gnoyr_VQ=FGK&QO_fu146_anzr=b0-gvzr"

driver_path = "c:/Users/user/Desktop/chromedriver_win32/chromedriver.exe"

driver = webdriver.Chrome(executable_path=driver_path)

driver.get(url)

driver.maximize_window()
sleep(3)


# 選擇資料格式
element = driver.find_element(By.ID,'chkshowNull')
element.click()


element = driver.find_element(By.ID,'chkDownloadZip')
element.click()

# 選擇資料欄位，睡眠時間是亂訂的，主要是不要跑太快讓網頁定位不到
element = driver.find_element(By.ID,'FL_DATE')
element.click()

sleep(2)

element = driver.find_element(By.ID,'MKT_UNIQUE_CARRIER')
element.click()

element = driver.find_element(By.ID,'TAIL_NUM')
element.click()

element = driver.find_element(By.ID,'ORIGIN')
element.click()

sleep(2)

element = driver.find_element(By.ID,'DEST')
element.click()

element = driver.find_element(By.ID,'CRS_DEP_TIME')
element.click()

element = driver.find_element(By.ID,'DEP_TIME')
element.click()

sleep(2)

element = driver.find_element(By.ID,'DEP_DELAY')
element.click()

element = driver.find_element(By.ID,'TAXI_OUT')
element.click()

element = driver.find_element(By.ID,'WHEELS_OFF')
element.click()

sleep(2)

element = driver.find_element(By.ID,'WHEELS_ON')
element.click()

element = driver.find_element(By.ID,'TAXI_IN')
element.click()

element = driver.find_element(By.ID,'ARR_TIME')
element.click()

sleep(2)

element = driver.find_element(By.ID,'ARR_DELAY_NEW')
element.click()

element = driver.find_element(By.ID,'DIVERTED')
element.click()

element = driver.find_element(By.ID,'CANCELLED')
element.click()

element = driver.find_element(By.ID,'CANCELLATION_CODE')
element.click()

sleep(2)

element = driver.find_element(By.ID,'CARRIER_DELAY')
element.click()

element = driver.find_element(By.ID,'WEATHER_DELAY')
element.click()

sleep(2)

element = driver.find_element(By.ID,'DIVERTED')
element.click()

element = driver.find_element(By.ID,'NAS_DELAY')
element.click()

element = driver.find_element(By.ID,'SECURITY_DELAY')
element.click()

element = driver.find_element(By.ID,'LATE_AIRCRAFT_DELAY')
element.click()

sleep(1)

# 用函式包裝起來
def get_airline_data(i,j):
    # 選擇年、月份
    element = Select(driver.find_element(By.ID,"cboYear"))
    element.select_by_index(i)
    element = Select(driver.find_element(By.ID,'cboPeriod'))
    element.select_by_index(j)
    
    sleep(2)
    
		# 把網頁捲到最上面，讓我網頁去找 Download 鍵
    js="var action=document.documentElement.scrollTop=0"
    driver.execute_script(js)
    
    sleep(1)
    
    element = driver.find_element(By.ID,'btnDownload')
    element.click()
    
    
    sleep(10)
    
# 這邊有一個問題點是有可能請求不到資料 e.g. 日期不正確 2022/12 根本還沒到，所以請求不到資料，
# 我這邊可能需要用 try...except... 來做包裝，但是那時候我沒注意所以分批爬取，之後有機會再優化
for i in range(0,5):
    for j in range(12):
        get_airline_data(i,j)
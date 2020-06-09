from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time 
from datetime import datetime,timedelta
import pytz
from pytz import timezone
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import itertools  
import re

driver = webdriver.Chrome("chromedriver.exe")
driver.maximize_window()
wait = WebDriverWait(driver, 20)
eastern = timezone('US/Eastern')
us_curr_time = datetime.now().astimezone(eastern).replace(tzinfo=None)
last_run_time = us_curr_time + timedelta(minutes=-20)
us_curr_time = us_curr_time.time()
last_run_time = last_run_time.time()
driver.get("https://www.globenewswire.com/")
main_div = wait.until(ec.visibility_of_element_located((By.XPATH,'//div[@class="rl-master-container"]')))
print(main_div) 
# time.sleep(10)
article = driver.find_elements_by_xpath('//div[@class="rl-container"]')
# print(len(article))
for a in article:
    # left_card = a.find_element_by_xpath('.//div[@class="col-sm-8 col-lg-9 pull-left card"]')
    link = a.find_element_by_xpath('.//h1/a')
    head = link.text
    # print(head)
    link = link.get_attribute("href")
    news_date = a.find_element_by_xpath('.//div[@class="meta-margin"]/p/span')
    news_date = news_date.text
    keyword = ["nasdaq","nyse","amex"]
    my_list = []    
    if "minutes" in news_date or "less than a minute ago"==news_date:           
        if "less than a minute ago"==news_date:
            if any(x in head for x in keyword):
                print(head)
                my_list.append(link)                           
                # print(link)
        else:            
            news_date = news_date[0:2]             
            news_date = int(news_date.replace(" ",""))
            # print(news_date)
            if news_date<=40:
                if any(x in head for x in keyword):
                    print(head)
                    my_list.append(link)                           
                    # print(link)
print("Current time",us_curr_time)
print(my_list)
print("Run Complete")
driver.close()        
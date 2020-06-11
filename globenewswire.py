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

def scrap_globenewswire(temp_minute):
    try:
        options  = webdriver.ChromeOptions()        
        options.add_argument('-headless')
        driver = webdriver.Chrome(options=options)
        wait = WebDriverWait(driver, 20)
        eastern = timezone('US/Eastern')
        us_curr_time = datetime.now().astimezone(eastern).replace(tzinfo=None)
        us_curr_time = us_curr_time.time()
        minutes = temp_minute
        driver.get("https://www.globenewswire.com/")
        main_div = wait.until(ec.visibility_of_element_located((By.XPATH,'//div[@class="rl-master-container"]')))
        print(main_div) 
        # time.sleep(10)
        article = driver.find_elements_by_xpath('//div[@class="rl-container"]')
        # print(len(article))
        my_list = []    
        for a in article:
            # left_card = a.find_element_by_xpath('.//div[@class="col-sm-8 col-lg-9 pull-left card"]')
            link = a.find_element_by_xpath('.//h1/a')
            head = str(link.text)
            head = head.lower()
            # print(head)
            link = link.get_attribute("href")
            news_date = a.find_element_by_xpath('.//div[@class="meta-margin"]/p/span')
            news_date = news_date.text
            keyword = ["nasdaq","nyse","amex"]
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
                    if news_date<=minutes:
                        if any(x in head for x in keyword):
                            my_list.append(link)                           
                            # print(link)
        print("Current time",us_curr_time)
        print(my_list)
        print("Run Complete")        
        return my_list
    except Exception as e:
        print("Something went Wrong!!",e)
    finally:
        driver.close()

if( __name__ == "__main__"):    
    my_list = scrap_globenewswire(4)
    print(my_list)    
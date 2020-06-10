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

def scrap_prnewswire(us_curr_time,last_run_time):
    try:
        options  = webdriver.ChromeOptions()        
        options.add_argument('-headless')
        driver = webdriver.Chrome(options=options)
        wait = WebDriverWait(driver, 20)
        print(us_curr_time)
        us_curr_time = us_curr_time.time()
        last_run_time = last_run_time.time()
        driver.get("https://www.prnewswire.com/news-releases/news-releases-list/")
        main_div = wait.until(ec.visibility_of_element_located((By.XPATH,'//div[@class="col-md-8 col-sm-8 card-list card-list-hr"]')))
        print(main_div) 
        # time.sleep(10)
        # article = driver.find_elements_by_xpath('//div[@class="@class="col-sm-12 card"]"]')
        # print(len(article))
        for a in itertools.chain(driver.find_elements_by_xpath('//div[@class="col-sm-8 col-lg-9 pull-left card"]'),driver.find_elements_by_xpath('//div[@class="col-sm-12 card"]')):    
            # left_card = a.find_element_by_xpath('.//div[@class="col-sm-8 col-lg-9 pull-left card"]')
            link = a.find_element_by_xpath('.//h3/a')
            head = link.text
            link = link.get_attribute("href")
            news_date = a.find_element_by_xpath('.//h3/small')
            # print(link)
            news_date = news_date.text
            ans = re.search("^\d\d:\d\d ET$",news_date)
            keyword = ["nasdaq","nyse","amex"]
            my_list = []    
            if(ans):        
                news_date = news_date.replace(" ET","")
                news_date = datetime.strptime(news_date,'%H:%M')
                news_date = news_date.time()
                if(last_run_time<news_date<us_curr_time):
                    if any(x in head for x in keyword):
                        print(head)
                        my_list.append(link)            
                        print(link)
            # break
        print("Current time",us_curr_time)        
        return my_list
    except Exception as e:
        print("Something went Wrong!!",e)
    finally:
        driver.close()            

if( __name__ == "__main__"):    
    eastern = timezone('US/Eastern')
    us_curr_time = datetime.now().astimezone(eastern).replace(tzinfo=None)
    last_run_time = us_curr_time + timedelta(minutes=-10)            
    my_list = scrap_prnewswire(us_curr_time,last_run_time)
    print(my_list)    
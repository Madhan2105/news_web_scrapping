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
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import logging

def scrap_globenewswire(us_curr_time,temp_minute,logger):
    try:
        logger.info("Globe:Scrapping...")
        print("Did changes 3",us_curr_time)
        print("temp_minute",temp_minute)
        options  = webdriver.ChromeOptions()        
        options.add_argument("--start-maximized")
        options.add_argument('-headless')
        options.add_argument("--log-level=3")
        driver = webdriver.Chrome(options=options)
        wait = WebDriverWait(driver, 20)
        eastern = timezone('US/Eastern')
        minutes = temp_minute
        logger.info("Globe:Opening Website")
        driver.get("https://www.globenewswire.com/")   
        main_div = wait.until(ec.visibility_of_element_located((By.XPATH,'//div[@class="rl-master-container"]')))
        article = driver.find_elements_by_xpath('//div[@class="rl-container"]')
        my_list = []                        
        logger.info("Globe:Iterating Article")
        print("Iterating Article")
        keyword = ["nasdaq","nyse","amex"]
        for a in article:               
            news_date = a.find_element_by_xpath('.//div[@class="meta-margin"]/p/span')
            news_date = news_date.text               
            if "minutes" in news_date or "less than a minute ago"==news_date:                                          
                logger.info("Globe:Article Found")
                if "less than a minute ago"==news_date:
                    logger.info("Globe:Article Found less than a minute ago")
                    print("inside less")
                    link = wait.until(lambda d: a.find_element_by_xpath('.//h1/a'))        
                    head = str(link.text)                    
                    link = str(link.get_attribute("href"))
                    my_list.append([link,head])                
                else:            
                    news_date = news_date[0:2]                             
                    news_date = int(news_date.replace(" ",""))
                    if news_date<=minutes:
                        logger.info("Globe:Article Found less than 4 minute ")
                        print("Minutes...")
                        link = wait.until(lambda d: a.find_element_by_xpath('.//h1/a'))          
                        head = str(link.text)                                                         
                        actions = ActionChains(driver)                
                        # print(link.text)
                        link = str(link.get_attribute("href"))
                        my_list.append([link,head])                        
        print(len(my_list))
        data_list = []
        logger.info("Globe:Iterating through link")
        if(my_list):
            for content in my_list:   
                driver.get(content[0])         
                data = wait.until(ec.visibility_of_element_located((By.XPATH,'//*[@id="content-L2"]/span')))
                data = data.text                
                data = data.lower()
                logger.info("Globe:Searching for keyword")
                if any(x in data for x in keyword):               
                    data_list.append(content)
                    print(content[1])            
        print("Current time",us_curr_time)
        print("Run Complete")        
        logger.info("Globe:Run Complete")
        driver.close()
        return data_list
    except Exception as e:
        print("Something went Wrong!!",e)
        logger.info("Exception")        
        logger.info(e)
        print("time ---",us_curr_time)
        driver.close()
        scrap_globenewswire(us_curr_time,temp_minute,logger)
    finally:
        pass
        # driver.close()

if( __name__ == "__main__"):    
    if(1):
        eastern = timezone('US/Eastern')        
        us_curr_time = datetime.now().astimezone(eastern).replace(tzinfo=None)    
        log_file  = "log/" + us_curr_time.date().strftime("%d_%m_%y") + ".log"
        print(log_file)        
        logging.basicConfig(filename=log_file, filemode='a', format='%(asctime)s %(message)s')
        logger=logging.getLogger()
        logger.setLevel(logging.INFO)    
        my_list = scrap_globenewswire(us_curr_time,60,logger)
        print(my_list)
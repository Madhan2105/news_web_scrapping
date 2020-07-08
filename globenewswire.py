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
import os

last_run_list = []
run_count = 0
def scrap_globenewswire(us_curr_time,temp_minute,logger):
    try:
        driver_flag = False        
        global my_list,run_count   
        run_count = run_count + 1 
        print(last_run_list)
        logger.info("Globe:Scrapping...")
        print("Did changes 4",us_curr_time)
        print("temp_minute",temp_minute)
        options  = webdriver.ChromeOptions()        
        options.add_argument("--start-maximized")
        options.add_argument("--no-sandbox")
        # options.binary_location = "/usr/bin/chromium-browser"
        options.add_argument('--headless')
        options.add_argument("--log-level=3")        
        cwd = os.getcwd()
        driver = webdriver.Chrome(cwd+"/Driver/chromedriver_globe",options=options)
        driver_flag = True       
        wait = WebDriverWait(driver, 20)
        eastern = timezone('US/Eastern')
        minutes = temp_minute
        flag = False
        data_list = []
        logger.info("Globe:3pages")
        for i in range(1,4):
            print("-----------"+str(i)+"----")
            url = "https://www.globenewswire.com/Index?page={}#pagerPos".format(i)
            # url = "https://www.globenewswire.com/NewsRoom"
            # https://www.globenewswire.com/Index?page=1#pagerPos
            logger.info("Globe:Opening Website")
            driver.get(url)   
            # cookies = wait.until(ec.visibility_of_element_located((By.XPATH,'//div[@class="action-container"]')))
            # driver.implicitly_wait(3)
            # cookies.click()
            # print("waiting")
            # wait.until(ec.invisibility_of_element_located((By.XPATH,'//div[@class="action-container"]')))
            # stock = wait.until(ec.visibility_of_element_located((By.XPATH,'//div[@rel="#facet-stockExchange"]')))
            # stock.click()
            # wait.until(ec.visibility_of_element_located((By.XPATH,'//*[@id="Exchange"]/li[6]'))).click()                        
            # import sys
            # sys.exit()
            # stock = wait.until(ec.visibility_of_element_located((By.XPATH,'//div[@id="facet-stockExchange"]')))
            # stock.click
            main_div = wait.until(ec.visibility_of_element_located((By.XPATH,'//div[@class="rl-master-container"]')))
            article = driver.find_elements_by_xpath('//div[@class="rl-container"]')
            my_list = []                        
            logger.info("Globe:Iterating Article")
            print("Iterating Article")
            # keyword = ["nasdaq","nyse","amex"]
            keyword = ["nasdaq","nyse","amex"]
            for a in article:               
                logger.info("Globe:Iterating...")                
                news_date = a.find_element_by_xpath('.//div[@class="meta-margin"]/p/span')
                news_date = news_date.text               
                logger.info(news_date)                
                if "minute" in news_date or "less than a minute ago"==news_date:                                          
                    print(news_date)
                    print("Globe:Article Found")
                    logger.info("Globe:Article Found")
                    if "less than a minute ago"==str(news_date):
                        logger.info("Globe:Article Found less than a minute ago")
                        print("inside less")
                        link = wait.until(lambda d: a.find_element_by_xpath('.//h1/a'))        
                        logger.info(str(link.text))                                           
                        head = str(link.text)                                           
                        logger.info(head) 
                        link = str(link.get_attribute("href"))
                        my_list.append([link,head])                
                    else:            
                        news_date = news_date[0:2]                             
                        news_date = int(news_date.replace(" ",""))
                        if news_date<minutes:
                            logger.info("Globe:Article Found less than 2 minute ")
                            print("Minutes...")
                            link = wait.until(lambda d: a.find_element_by_xpath('.//h1/a'))          
                            logger.info(str(link.text))                   
                            head = str(link.text)                                                                                     
                            logger.info(head) 
                            # actions = ActionChains(driver)                
                            # print(link.text)
                            link = str(link.get_attribute("href"))
                            my_list.append([link,head])                        
                        else:
                            logger.info("Globe:No More Articles")
                            flag = True
                            break
            print(len(my_list))
            if(my_list):
                logger.info("Globe:Iterating through link")
                for index,content in enumerate(my_list):   
                    print(content[0])
                    driver.get(content[0])         
                    data = wait.until(ec.visibility_of_element_located((By.XPATH,'//*[@id="content-L2"]/span')))
                    data = data.text                
                    data = data.lower()
                    logger.info("Globe:Searching for keyword")
                    if any(x in data for x in keyword):               
                        data_list.append(content)
                        last_run_list.append(content)
                        print(content[1])            
            if(flag):
                break
        driver.close()
        print("Current time",us_curr_time)
        print("Run Complete")        
        logger.info("Globe:Run Complete")
        return data_list
    except Exception as e:
        # last_run_list = my_list
        print("Something went Wrong!!",e)
        logger.info("Exception")        
        logger.info(e)
        print("time ---",us_curr_time)
        if(driver_flag):
            driver.close()                
        if(run_count<=2):            
            my_list = scrap_globenewswire(us_curr_time,10,logger)
        # driver.close()
        # scrap_globenewswire(us_curr_time,temp_min ute,logger)
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
        my_list = scrap_globenewswire(us_curr_time,1000,logger)
        print(my_list)

# cookies = wait.until(ec.visibility_of_element_located((By.XPATH,'/html/body/div[6]/div/div')))
# cookies.click()
# time.sleep(5)
# stock = wait.until(ec.visibility_of_element_located((By.XPATH,'//div[@rel="#facet-stockExchange"]')))
# stock.click()
# wait.until(ec.visibility_of_element_located((By.XPATH,'//*[@id="Exchange"]/li[6]'))).click()            
# wait.until(ec.visibility_of_element_located((By.XPATH,'//input[@id="facetfield_Exchange_nasdaq"]'))).click()                        
# # wait.until(ec.visibility_of_element_located((By.XPATH,'//input[@value="NYSE"]'))).click()                                    
# # wait.until(ec.visibility_of_element_located((By.XPATH,'//input[@value="AMEX"]'))).click()                        
# main_div = wait.until(ec.visibility_of_element_located((By.XPATH,'//div[@id="content-R3"]')))
# article = driver.find_elements_by_xpath('//div[@class="results-link"]')        
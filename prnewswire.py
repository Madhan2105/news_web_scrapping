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

my_list = []
run_count = 0
def scrap_prnewswire(us_curr_time,last_run_time,logger):
    try:
        driver_flag = False        
        global my_list,run_count   
        run_count = run_count + 1 
        logger.info("Prn:Scrapping....")
        options  = webdriver.ChromeOptions()        
        options.add_argument("--start-maximized")
        options.binary_location = "/usr/bin/chromium-browser"
        options.add_argument('--headless')
        options.add_argument("--log-level=3")        
        cwd = os.getcwd()
        driver = webdriver.Chrome(cwd+"/Driver/chromedriver_prn",options=options)        
        driver_flag = True       
        wait = WebDriverWait(driver, 20)
        print(us_curr_time)
        if(run_count<=1):
            us_curr_time = us_curr_time.time()
            # last_run_time = last_run_time.time()
            last_run_time = last_run_time.time().replace(second=0, microsecond=0)
            print(last_run_time)    
        driver.get("https://www.prnewswire.com/news-releases/news-releases-list/?page=1&pagesize=50")
        try:
            print("Reading txt tile")
            logger.info("Reading txt tile")
            f = open("prn.txt", "r")
            last_run = f.read()
            last_run = last_run.split(";")
            print(last_run)
        except:
            logger.info("Except of read file")
            print("inside excpet of read file")
            last_run = []        
        main_div = wait.until(ec.visibility_of_element_located((By.XPATH,'//div[@class="col-md-8 col-sm-8 card-list card-list-hr"]')))
        print(main_div) 
        my_list = []    
        keyword = ["nasdaq","nyse","amex"]
        logger.info("Prn:Iterating Article")
        article = driver.find_elements_by_xpath('//div[@class="col-sm-8 col-lg-9 pull-left card"]')
        article1 = driver.find_elements_by_xpath('//div[@class="col-sm-12 card"]')
        logger.info("------------First Loop------------")        
        for a in article:
            print("inside first")
            # left_card = a.find_element_by_xpath('.//div[@class="col-sm-8 col-lg-9 pull-left card"]')            
            link = a.find_element_by_xpath('.//h3/a')
            head = link.text
            print(head)
            news_date = a.find_element_by_xpath('.//h3/small')
            # print(link)
            news_date = news_date.text
            logger.info(head)
            logger.info(news_date)
            ans = re.search("^\d\d:\d\d ET$",news_date)
            if(ans):        
                logger.info("Prn:Found Article")
                news_date = news_date.replace(" ET","")
                news_date = datetime.strptime(news_date,'%H:%M')
                news_date = news_date.time()
                print("news_date",news_date)
                if(last_run_time<=news_date):
                    temp_head = link.text
                    print(temp_head)
                    res = [i for i in last_run if temp_head in i] 
                    if(res):
                        logger.info("Found value last run")     
                        continue                  
                    print(":inside")
                    logger.info("Prn:Article filtered")
                    # print(head)
                    actions = ActionChains(driver)            
                    actions.key_down(Keys.CONTROL).click(link).key_up(Keys.CONTROL).perform()
                    link = str(link.get_attribute("href"))
                    driver.switch_to.window(driver.window_handles[-1])
                    # driver.get(link)                
                    data = wait.until(ec.visibility_of_all_elements_located((By.XPATH,'//div[@class="col-sm-10 col-sm-offset-1"]')))
                    content = ""
                    for child in data:
                        # print(child.text)
                        content = content + str(child.text)
                    # print("----------------------------")
                    # print("data",content)
                    driver.close()                
                    driver.switch_to.window(driver.window_handles[0])
                    content = content.lower()
                    logger.info("Prn:Searching for Keyword")
                    if any(x in content for x in keyword):
                        # print(head)
                        my_list.append([link,head])                        
                        # print(link)
                else:
                    break
            print("--------------------------outer")
            try:
                f = open("prn.txt", "a")
                f.write(str(head)+";")                        
                f.close()            
            except:
                pass            
        logger.info("------------Second Loop------------")        
        for a in article1:
            # left_card = a.find_element_by_xpath('.//div[@class="col-sm-8 col-lg-9 pull-left card"]')
            link = a.find_element_by_xpath('.//h3/a')
            head = link.text
            print(head)
            news_date = a.find_element_by_xpath('.//h3/small')
            # print(link)
            news_date = news_date.text
            logger.info(news_date)
            logger.info(head)
            ans = re.search("^\d\d:\d\d ET$",news_date)
            if(ans):        
                logger.info("Prn:Found Article 2")
                news_date = news_date.replace(" ET","")
                news_date = datetime.strptime(news_date,'%H:%M')
                news_date = news_date.time()
                print("news_date",news_date)
                if(last_run_time<=news_date):
                    temp_head = link.text
                    print(temp_head)
                    res = [i for i in last_run if temp_head in i] 
                    if(res):
                        logger.info("Found value last run")     
                        continue                       
                    print(":inside")
                    logger.info("Prn:Article filtered")
                    # print(head)
                    actions = ActionChains(driver)            
                    actions.key_down(Keys.CONTROL).click(link).key_up(Keys.CONTROL).perform()
                    link = str(link.get_attribute("href"))
                    driver.switch_to.window(driver.window_handles[-1])
                    # driver.get(link)                
                    data = wait.until(ec.visibility_of_all_elements_located((By.XPATH,'//div[@class="col-sm-10 col-sm-offset-1"]')))
                    content = ""
                    for child in data:
                        # print(child.text)
                        content = content + str(child.text)
                    # print("----------------------------")
                    # print("data",content)
                    driver.close()                
                    driver.switch_to.window(driver.window_handles[0])
                    content = content.lower()
                    logger.info("Prn:Searching for Keyword")
                    if any(x in content for x in keyword):
                        print("Value found")
                        # print(head)
                        my_list.append([link,head])                        
                        # print(link)
                else:
                    break           
            print("--------------------------outer")
            try:
                f = open("prn.txt", "a")
                f.write(str(head)+";")                        
                f.close()            
            except:
                pass    
            # break
            # print(my_list)
        print("Current time",us_curr_time)        
        logger.info("Prn:Run Complete")
        driver.close()
        return my_list

    except Exception as e:
        print("Something went Wrong!!",e)
        logger.info("Exception")
        logger.info(e)
        if(driver_flag):
            driver.close()        
        if(run_count<=2):
            scrap_prnewswire(us_curr_time,last_run_time,logger)        
    finally:
        my_list = []
        run_count = 0            
        open('prn.txt', 'w').close()

if( __name__ == "__main__"):    
    temp_minute = 60
    eastern = timezone('US/Eastern')        
    us_curr_time = datetime.now().astimezone(eastern).replace(tzinfo=None)    
    last_run_time = us_curr_time - timedelta(minutes=temp_minute)
    log_file  = "log/" + us_curr_time.date().strftime("%d_%m_%y") + ".log"
    print(log_file)        
    logging.basicConfig(filename=log_file, filemode='a', format='%(asctime)s %(message)s')
    logger=logging.getLogger()
    logger.setLevel(logging.INFO)    
    my_list = scrap_prnewswire(us_curr_time,last_run_time,logger)
    print(my_list)    
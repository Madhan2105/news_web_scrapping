from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time 
from datetime import datetime,timedelta
from pytz import timezone
import pytz
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import logging
import os
import setting

run_count = 0
def scrap_bussinewire(us_curr_time,last_run_time,logger):
    try:
        driver_flag = False        
        global run_count
        run_count = run_count + 1 
        print("run_count",run_count)
        logger.info("Buss:Scrapping...")
        options  = webdriver.ChromeOptions()        
        options.add_argument("--start-maximized")
        # options.binary_location = "/usr/bin/chromium-browser"
        options.add_argument("--no-sandbox")
        options.add_argument('--headless')
        options.add_argument("--log-level=3")        
        cwd = os.getcwd()
        driver = webdriver.Chrome(cwd+"/Driver/chromedriver_buss",options=options)
        driver_flag = True        
        wait = WebDriverWait(driver, 20)
        print(us_curr_time)
        driver.get("https://www.businesswire.com/portal/site/home/news/")        
        # my_list = []
        flag = False
        logger.info("Buss:Iterating 3pages")
        try:
            print("Reading txt tile")
            logger.info("Buss:Reading txt tile")
            f = open("buss.txt", "r")
            last_run = f.read()
            last_run = last_run.split(";")
            print(last_run)
        except:
            logger.info("Empty list ")
            print("inside excpet of read file")
            last_run = []
        for row in range(1,20):
            logger.info(row)
            print("-----"+str(row)+"-----")            
            main_div = wait.until(ec.visibility_of_element_located((By.XPATH,'//ul[@class="bwNewsList"]')))
            print(main_div) 
            # time.sleep(10)
            article = main_div.find_elements_by_xpath('//div[@itemscope="itemscope"]')
            print(len(article))
            logger.info("Buss:Iterating Article")
            for a in article:    
                logger.info("Buss:Iterating...")
                print("Iterating...")
                # print(a)    
                link = a.find_element_by_xpath('.//a[@class="bwTitleLink"]')
                # print(last_run)
                # print("after check")
                # print(link.get_attribute("href"))
                # link = head.find_element_by_xpath('.//a')                
                date_element  = a.find_element_by_xpath('.//time[@itemprop="dateModified"]')
                # print(date_element.text)
                news_date = date_element.text
                # news_date = news_date.replace(" EST","")
                news_date = datetime.strptime(news_date,'%m/%d/%Y - %I:%M %p')
                logger.info("news_date")
                logger.info(news_date)
                logger.info(link.text)
                # print(news_date)
                keyword = ["nasdaq","nyse","amex"]
                if(last_run_time<news_date):
                    if(last_run):     
                        logger.info("checking for value in last run")     
                        temp_head = link.text
                        print(temp_head)
                        res = [i for i in last_run if temp_head in i] 
                        if(res):
                            logger.info("Found value last run")     
                            continue
                    logger.info("Buss:Found Article")
                    actions = ActionChains(driver)            
                    head = link.text
                    actions.key_down(Keys.CONTROL).click(link).key_up(Keys.CONTROL).perform()
                    link = link.get_attribute("href")
                    driver.switch_to.window(driver.window_handles[-1])
                    data = wait.until(ec.visibility_of_element_located((By.XPATH,'//div[@class="bw-release-story"]')))
                    data = data.text
                    # print("----------------------------")
                    # print("data",data)
                    driver.close()                
                    driver.switch_to.window(driver.window_handles[0])
                    data = data.lower()
                    logger.info("Buss:Searching keyword")
                    # print(data)
                    if any(x in data for x in keyword):
                        setting.buss_my_list.append([link,head])
                    print("------------------------------------------------")
                    print(setting.buss_my_list)
                else:
                    logger.info("Buss:No More Articles")                    
                    flag = True
                    break
                try:
                    f = open("buss.txt", "a")
                    f.write(str(head)+";")                        
                    f.close()            
                except:
                    pass
            if(flag):
                break
            next = wait.until(ec.visibility_of_element_located((By.XPATH,'//*[@id="paging"]/div[2]/div[2]')))
            next.click()
                # print(link.get_attribute("href"))
            # break
        driver.close()
        print("*******")
        print(setting.buss_my_list)            
        return setting.buss_my_list            
        # return temp_list            
    except Exception as e:
        print("Something went Wrong!!",e)
        print(setting.buss_my_list)
        logger.info("Exception")
        logger.info(e)
        if(driver_flag):
            driver.close()        
        # driver.close()
        if(run_count<=2):            
            scrap_bussinewire(us_curr_time,last_run_time,logger)
        logger.info("Tried more the twice")
    finally:
        run_count = 0        
        open('buss.txt', 'w').close()
        logger.info("Executing finally bllock")

if( __name__ == "__main__"):    
    eastern = timezone('US/Eastern')     
    temp_minute = 2
    us_curr_time = datetime.now().astimezone(eastern).replace(tzinfo=None)    
    last_run_time = us_curr_time - timedelta(minutes=temp_minute)
    log_file  = "log/" + us_curr_time.date().strftime("%d_%m_%y") + ".log"
    print(log_file)        
    logging.basicConfig(filename=log_file, filemode='a', format='%(asctime)s %(message)s')
    logger=logging.getLogger()
    logger.setLevel(logging.INFO)    
    scrap_bussinewire(us_curr_time,last_run_time,logger)
    print(setting.buss_my_list)
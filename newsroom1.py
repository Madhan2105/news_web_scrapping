from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time 
from datetime import datetime,timedelta
import pytz
from pytz import timezone
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import discord
from dotenv import load_dotenv
from discord.ext import commands, tasks
import asyncio
import os
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import logging

my_list = []
run_count = 0
def newsroom_scrap(us_curr_time,last_run_time,logger):
    try:     
        global my_list,run_count   
        run_count = run_count + 1 
        print(datetime.now())
        logger.info("Newsroom : Scrapping..")
        options  = webdriver.ChromeOptions()        
        options.add_argument('-headless')
        options.add_argument("--log-level=3")        
        cwd = os.getcwd()
        driver = webdriver.Chrome(cwd+"/Driver/chromedriver_news",options=options)        
        wait = WebDriverWait(driver, 20)
        print(us_curr_time)
        # last_run_time = last_run_time.time().replace(second=0, microsecond=0)
        driver.get("https://www.accesswire.com/newsroom/")
        try:
            print("Reading txt tile")
            logger.info("News:Reading txt tile")
            f = open("news.txt", "r")
            last_run = f.read()
            last_run = last_run.split(";")
            print(last_run)
        except:
            print("inside excpet of read file")
            last_run = []

        logger.info("Newsroom : Opening Website")
        main_div = wait.until(ec.visibility_of_element_located((By.XPATH,'//div[@class="w-embed"]')))
        print(main_div) 
        # time.sleep(10)
        article = main_div.find_elements_by_xpath('//div[@class="w-col w-col-9"]')
        print(len(article))
        logger.info("Newsroom : Iterating Article")
        for a in article:              
            logger.info("Iterating...")
            # print(a)    
            head = a.find_element_by_xpath('.//div[@class="headlinelink"]')
            # print(head)
            link = head.find_element_by_xpath('.//a')            
            date_element  = a.find_element_by_xpath('.//div[@class="date"]')
            news_date = date_element.text
            news_date = news_date.replace(" EST","")
            news_date = datetime.strptime(news_date,'%A, %B %d, %Y %I:%M %p')
            logger.info(news_date)
            logger.info(str(link.text))
            keyword = ["nasdaq","nyse","amex"]
            print(link.text)
            logger.info("Executing finally bllock")
            if(last_run_time<=news_date):
                if(last_run):     
                    logger.info("checking for value in last run")     
                    temp_head = link.text
                    print(temp_head)
                    res = [i for i in last_run if temp_head in i] 
                    if(res):
                        logger.info("Found value last run")     
                        continue                  
                logger.info("Newsroom : Article Found")
                # link.click()
                print(head.text)
                actions = ActionChains(driver)         
                logger.info("Newsroom : Opening Tab")   
                actions.key_down(Keys.CONTROL).click(link).key_up(Keys.CONTROL).perform()
                head = head.text
                link = str(link.get_attribute("href"))                    
                driver.switch_to.window(driver.window_handles[-1])
                # driver.get(link)                
                data = wait.until(ec.visibility_of_element_located((By.XPATH,'//*[@id="Article"]/div[4]')))
                data = data.text
                # print("----------------------------")
                # print("data",data)
                driver.close()                
                driver.switch_to.window(driver.window_handles[0])
                data = data.lower()
                logger.info("Newsroom : Searching for keyword")
                if any(x in data for x in keyword):
                    my_list.append([link,head])
                print(my_list)
            else:                
                logger.info("No More Aricle")
                break

            try:
                f = open("news.txt", "a")
                f.write(str(head)+";")                        
                f.close()            
            except:
                pass
                
        logger.info("Newsroom : Run Succesfully")
        print("Run Succesfully")
        print(us_curr_time)
        driver.close()    
        return my_list
    except Exception as e:
        print("Something went Wrong!!",e)
        logger.info("Exception")
        logger.info(e)
        # driver.close()
        newsroom_scrap(us_curr_time,last_run_time,logger)
    finally:
        my_list = []
        run_count = 0        
        open('news.txt', 'w').close()
        logger.info("Executing finally bllock")

if( __name__ == "__main__"):
    eastern = timezone('US/Eastern')     
    temp_minute = 3000
    us_curr_time = datetime.now().astimezone(eastern).replace(tzinfo=None)    
    last_run_time = us_curr_time - timedelta(minutes=temp_minute)
    log_file  = "log/" + us_curr_time.date().strftime("%d_%m_%y") + ".log"
    print(log_file)        
    logging.basicConfig(filename=log_file, filemode='a', format='%(asctime)s %(message)s')
    logger=logging.getLogger()
    logger.setLevel(logging.INFO)    
    my_list = newsroom_scrap(us_curr_time,last_run_time,logger)
    print(my_list)
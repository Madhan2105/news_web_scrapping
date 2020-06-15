from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time 
from datetime import datetime,timedelta
import pytz
from pytz import timezone
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import logging
def scrap_bussinewire(us_curr_time,last_run_time,logger):
    try:
        logger.info("Buss:Scrapping...")
        options  = webdriver.ChromeOptions()        
        options.add_argument('-headless')
        options.add_argument("--log-level=3")        
        driver = webdriver.Chrome(options=options)
        wait = WebDriverWait(driver, 20)
        print(us_curr_time)
        driver.get("https://www.businesswire.com/portal/site/home/news/")        
        my_list = []
        logger.info("Buss:Iterating 3pages")
        for row in range(1,4):
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
                # print(link.get_attribute("href"))
                # link = head.find_element_by_xpath('.//a')                
                date_element  = a.find_element_by_xpath('.//time[@itemprop="dateModified"]')
                # print(date_element.text)
                news_date = date_element.text
                # news_date = news_date.replace(" EST","")
                news_date = datetime.strptime(news_date,'%m/%d/%Y - %I:%M %p')
                # print(news_date)
                keyword = ["nasdaq","nyse","amex"]
                if(last_run_time<news_date<us_curr_time):
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
                    if any(x in data for x in keyword):
                        my_list.append([link,head])
                    # print(my_list)
                else:
                    logger.info("Buss:No More Articles")                    
                    break
            next = wait.until(ec.visibility_of_element_located((By.XPATH,'//*[@id="paging"]/div[2]/div[2]')))
            next.click()
                # print(link.get_attribute("href"))
            # break
        # print(my_list)
        return my_list    
    except Exception as e:
        print("Something went Wrong!!",e)
        logger.info("Exception")
        logger.info(e)
    finally:
        driver.close()    

if( __name__ == "__main__"):    
    eastern = timezone('US/Eastern')     
    temp_minute = 60   
    us_curr_time = datetime.now().astimezone(eastern).replace(tzinfo=None)    
    last_run_time = us_curr_time - timedelta(minutes=temp_minute)
    log_file  = "log/" + us_curr_time.date().strftime("%d_%m_%y") + ".log"
    print(log_file)        

    logging.basicConfig(filename=log_file, filemode='a', format='%(asctime)s %(message)s')
    logger=logging.getLogger()
    logger.setLevel(logging.INFO)    
    my_list = scrap_bussinewire(us_curr_time,last_run_time,logger)
    print(my_list)
import os
import time
import shutil
from datetime import datetime 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless") 
chrome_options.add_argument("--disable-dev-shm-usage")

def difference_time (time_1, time_2):
      difference_time = time_2 - time_1
      difference_milliseconds = difference_time.total_seconds() * 1000
      #difference_milliseconds -= 15000
      return difference_milliseconds

def requests_url (url):
    try:
        driver.get(url)
        return "successful request"
    except Exception as e:
        return "failed request"

sites_web = [
    #taken from: https://www.similarweb.com/top-websites/
    "https://www.google.com",
    "https://www.live.com",
    "https://www.twitter.com",
    "https://www.youtube.com",
    "https://www.instagram.com",
    "https://www.baidu.com",
    "https://www.twitter.com",
    "https://www.wikipedia.com",
    "https://www.yahoo.com",
    "https://www.whatsapp.com"
]

result_file = "results_chrome.txt"
request_number = 0

while True:

    request_number += 1 
    current_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print(f"\nResults of {current_date} --> {request_number}\n")   
    
    with open(result_file, "a") as file:  

        file.write(f"\nResults of {current_date}\n")

        for url in sites_web:
            
            time_1 = datetime.now()
            
            try:
                driver = webdriver.Chrome(options=chrome_options)
            
                #time.sleep(15)

                response = requests_url(url)
                time_2 = datetime.now()
                difference_milliseconds = difference_time(time_1, time_2)
                file.write(f"{url}|{time_1}|{time_2}|{difference_milliseconds}|{response}|Google Chrome DID run\n")

            except Exception as e:

                time.sleep(15)
                time_2 = datetime.now()
                difference_milliseconds = difference_time(time_1, time_2)
                file.write(f"{url}|{time_1}|{time_2}|{difference_milliseconds}|Google Chrome DIDN'T run\n")
                #file.write(f"Error: {str(e)}\n")
                #driver.quit()
                continue
                    
            driver.quit()

            print(f"------------------- request to {url} finished\n")
            time.sleep(5)

    #backup to results_chrome.txt
    file_backup = "results_chrome.txt"
    current_date = datetime.now().strftime("%d-%m-%Y %H-%M-%S")
    path_backup = "D:\\results_chrome"
    name_backup = f"results_chrome_{current_date}.txt"
    path_file_backup = os.path.join(path_backup, name_backup)
    shutil.copy2(file_backup, path_file_backup)
    print("------------------- file results_chrome.txt backup done\n")        
         
    print("------------------- script sleeping for 30 minutes\n")
    time.sleep(1800)  #sleep for 30 min (1800seg)


YBvKfYFj6PzEHMb
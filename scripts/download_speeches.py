import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

'''
NOT FINISHED YET

TODO
    - Redo speech downloading (using requests instead of vising pages with selenium)
    - Add some arguments for only downloading certain sets or start and stop
    - Better error handling for duplicate subdirs
    - Better commenting...
'''


browser = webdriver.Chrome(executable_path=f"{os.getcwd()}\\bin\\webdriver\\chromedriver.exe")

browser.get("https://millercenter.org/the-presidency/presidential-speeches")

# Getting list of president's names
president_list = browser.find_elements_by_class_name("option")
browser.find_elements_by_xpath("")

#Creating subdirs for president's
# ONLY RUN ONCE !!!

#exit()
for i in range(len(president_list)):
    time.sleep(1)
    #Choose president
    curr_pres = browser.find_elements_by_class_name("option")[i]
    
    name = curr_pres.text
    speeches_dir = "raw-speeches\\" + name
    os.mkdir(speeches_dir)
    curr_pres.click()
    time.sleep(2)
    print(f"On president: {name}")
    #Scroll all the way down the page (to load all transcripts)
    num = 0
    new_num = 1
    while num != new_num:
        speech_links = browser.find_elements_by_class_name("field-content")
        num = len(speech_links)
        browser.execute_script("window.scrollBy(0,document.body.scrollHeight)")
        time.sleep(1)
        speech_links = browser.find_elements_by_class_name("field-content")
        new_num = len(speech_links)
    
    num_speeches = len(speech_links)
    browser.execute_script(f"window.scrollBy(0,-(document.body.scrollHeight))")

    for i in range(0,num_speeches,2):
        browser.find_elements_by_class_name("field-content")[i].click()

        speech_title_elemenet = WebDriverWait(browser,4).until(EC.presence_of_element_located((By.CLASS_NAME, "presidential-speeches--title")))

        title = browser.find_element_by_class_name("presidential-speeches--title").text
        speech = browser.find_element_by_class_name("view-transcript").text

        colon = title.index(":")
        date = title[:colon]
        speech_title = title[colon+2:]
        file_title = "".join([x.title() for x in speech_title.split(' ')])

        file_dir = speeches_dir + "\\" + file_title + ".txt"
        f = open(file_dir, "w")
        f.write(speech)
        f.close()
        print(f"Wrote {file_title}")

        browser.back()
        president_filter = WebDriverWait(browser, 2).until(EC.presence_of_element_located((By.ID, "block-sitebranding-2")))
        president_filter.click()
        time.sleep(1)
        president_filter.click()
        

    
    browser.find_elements_by_class_name("option")[i].click()
    time.sleep(2)

    

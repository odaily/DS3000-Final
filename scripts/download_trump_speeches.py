import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import requests
import urllib.request as urllib
from lxml import html


# Load html into soup
site = open('trump_speeches_index.html')
tree = html.fromstring(site.read())
site.close()

date_titles = tree.xpath('//span[@class="field-content"]/a/text()')
wanted_links = tree.xpath('//span[@class="field-content"]/a')
hrefs = []

for hyperlink in wanted_links:
    hrefs.append(hyperlink.attrib['href'])

for link in hrefs:
    r = requests.get(link)
    soup = r.text
print(hrefs)


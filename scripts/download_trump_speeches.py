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

index = 0
for link in hrefs:
    r = requests.get(link)
    r.encoding = 'utf-8'
    page = html.fromstring(r.content)
    transcript_tag = page.xpath('//div[@class="transcript-inner"]')[0]
    paras = transcript_tag.xpath('./p/text()')
    # Stupid exception because of ONE speech
    # https://millercenter.org/the-presidency/presidential-speeches/february-5-2019-state-union-address
    # Stores transcript within a <main> within the transcript-inner
    # The only one that does this ._.
    if len(paras) == 0:
        paras = transcript_tag.xpath('./main/p/text()')
    paras = [p for p in paras if not p.startswith("AUDIENCE")]
    transcript = '\n'.join(paras)

    title = date_titles[index]
    colon = title.index(":")
    date = title[:colon]
    speech_title = title[colon+2:]

    speech_index = f"{index:3}".replace(' ', '0')
    file_name = f"trump_speeches_{speech_index}.txt"
    f = open(f'trump/{file_name}', 'w+', encoding='utf-8')
    f.write(f'<title="{speech_title}">\n')
    f.write(f'<date="{date}">\n')
    f.write(transcript)
    f.close()
    index += 1

print(hrefs)


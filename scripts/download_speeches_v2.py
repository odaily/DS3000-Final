import argparse
import os
import lxml.html
import requests

from bs4 import BeautifulSoup

## Load main page
main_url = "https://millercenter.org/the-presidency/presidential-speeches"
main_req = requests.get(main_url)
main_page = lxml.html.fromstring(main_req.content)

## Get president's names and search IDs
pres_tags = main_page.xpath('//input[@class="form-checkbox"]')
pres_ids = [elem.get('value') for elem in pres_tags]
pres_names = main_page.xpath('//label[@class="option"]/text()')
pres_names = [name.replace(' ','').replace('.','') for name in pres_names]

## Just in case, idk why
if len(pres_ids) != len(pres_names):
    raise IndexError("Unequal number of president names and IDs")

## Loop the thang
for i in range(len(pres_ids)):
    pres = pres_names[i]
    url_id = pres_ids[i]

    # GET page already filtered for given president
    filtered_url = main_url + f"?field_president_target_id%5B{url_id}%5D={url_id}#selected-tags"
    speeches_source = requests.get(filtered_url)
    speeches_doc = lxml.html.fromstring(speeches_source.content)

    
    # Set up directory to hold speeches
    parent_dir = "raw-speeches\\" + pres
    os.mkdir(parent_dir)
    print("Created directory for ", pres)
    
    # Finding speech hyperlinks
    speech_rows = speeches_doc.xpath('//div[@class="views-field views-field-title"]')
    for tag in speech_rows:
        # Extract data from page HTML
        speech_hyperlink = tag.xpath('./span[@class="field-content"]/a')[0]
        speech_title = speech_hyperlink.xpath('./text()')[0]
        speech_href = speech_hyperlink.get('href');
        
        # Clean up for using later
        colon_index = speech_title.index(":")
        speech_date = speech_title[:colon_index]
        speech_title = speech_title[colon_index+2:]
        file_title = speech_title.replace(' ', '')

        # Request for speech's page
        speech_page = requests.get("https://millercenter.org" + speech_href)
        speech_source = lxml.html.fromstring(speech_page.content)
        transcript_tag = speech_source.xpath("//div[@class='view-transcript']")[0]
        paras = transcript_tag.xpath("./p/text()")
        transcript = '\n'.join(paras)

        # Write transcript to file
        path = f"{parent_dir}/{file_title}.txt"
        f = open(path, '+w')
        f.write(transcript)
        f.close()
        print(f"Saved {speech_title} to {file_title}.")

        
    exit()
    

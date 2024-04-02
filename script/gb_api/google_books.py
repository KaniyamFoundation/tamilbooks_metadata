#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup 
import random
import pandas as pd
import json
import os
import urllib.request 
from time import sleep
import subprocess
from time import sleep


# Tamil
# Tamil+Language
# தமிழ்
# ஈழம்
# இலக்கணம்
# இலக்கியம்
# வரலாறு

# In[ ]:


# Constants
# Export folder
GOOGLE_API_KEY = ""
DATA_FOLDER = "google_books_data"
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)
DOWNLOAD_REPORT_FILE = DATA_FOLDER + "/google_books_download_report.csv"


# In[ ]:


# Load download status file
if not os.path.exists(DOWNLOAD_REPORT_FILE):
    work_metadata_df = pd.DataFrame(columns=['identifier','location_url'])
else:
    work_metadata_df = pd.read_csv(DOWNLOAD_REPORT_FILE)
work_metadata_df.shape


# In[ ]:


def get_work_metadata(item_json):
    work_dict = {}
    work_dict["identifier"] = item_json["id"]
    work_dict["location_url"] = item_json["selfLink"]
    work_dict["accessInfo"] = item_json["accessInfo"]
    volumeInfo = item_json["volumeInfo"]
    for value_label, value in volumeInfo.items():
        work_dict[value_label] = value
    return work_dict


# In[ ]:


query_str = 'அறிவியல்'
my_response_1 = requests.get("https://www.googleapis.com/books/v1/volumes?q="+ query_str +"&filter=full&key=" + GOOGLE_API_KEY + "&startIndex=0&maxResults=40")
gb_json_results_1 = json.loads(my_response_1.content)


# In[ ]:


total_items = int(gb_json_results_1["totalItems"])
count = 0
while count <= total_items:
    print("processing " + str(count) + " of " + str(total_items))
    my_response = requests.get("https://www.googleapis.com/books/v1/volumes?q="+ query_str +"&filter=full&key=" + GOOGLE_API_KEY + "&startIndex="+ str(count) + "&maxResults=40")
    gb_json_results = json.loads(my_response.content)
    work_items = gb_json_results["items"]
    for work_json in work_items:
        work_identifier = work_json["id"]
        if work_identifier not in work_metadata_df["identifier"].values:
            work_dict = get_work_metadata(work_json)
            work_metadata_df = pd.concat([work_metadata_df, pd.DataFrame([work_dict])], ignore_index=True)
            work_metadata_df.to_csv(DOWNLOAD_REPORT_FILE, index=False)
        else:
            print("Existing identifier found " + work_identifier)
    
    count = count + 40
    sleep(10)


# In[ ]:





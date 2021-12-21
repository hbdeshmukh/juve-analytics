# -*- coding: utf-8 -*-
"""
Created on Mon Dec 20 14:30:48 2021

This script scrapes the match reports for a specified season and dump them into
csv files

To run this script, a browser executable needs to be downloaded from
https://www.selenium.dev/documentation/webdriver/getting_started/install_drivers/
and put on the path

Data taken from fbref.com

@author: timot
"""


import time
from bs4 import BeautifulSoup
from selenium.webdriver import Remote
from selenium.webdriver.chrome.service import Service
import pandas as pd
import os

# Start server and extract urls for a specific season

s = Service(executable_path="./chromedriver") # Adjust the path accordingly
s.start()

season = 21
year = '20{}-20{}'.format(season, season+1)
url = "https://fbref.com/en/squads/e0652b02/{}/Juventus-Stats".format(year)
juve_id = 'e0652b02'

driver = Remote(s.service_url)
driver.get(url)
content = driver.page_source
soup = BeautifulSoup(content, "lxml")
temp = soup.findAll(attrs={"data-stat": "match_report"})

time.sleep(1)
driver.close()

s.stop()

urls = []
for i in range(len(temp)):
    if temp[i].findChild('a') is not None and temp[i].text == 'Match Report':
        urls.append("https://fbref.com{}".format(temp[i].findChild('a')['href']))

# Each element in the urls list contains a url for a match report
# Loop over them and extract the shot table as a csv file

s = Service(executable_path="./chromedriver") # Adjust the path accordingly
s.start()

for i in range(len(urls)):
    # Open the url of the match report
    driver = Remote(s.service_url)
    driver.get(urls[i])
    
    content = driver.page_source
    soup = BeautifulSoup(content, "lxml")
    
    df = soup.find('table', attrs={'id': 'shots_all'})
    
    time.sleep(1)
    driver.close()
    
    # Convert table to dataframe and clean the table
    
    df = pd.read_html(str(df))[0]
    df = df.droplevel(0, axis=1) # Clear the first level header
    df = df.iloc[:,:7]
    df.dropna(subset=['Minute'], inplace=True)
    df.fillna('', inplace=True)
    
    # Dump data to a csv file for each match report
    data_root_path = os.path.abspath("../../data/match_data/{}-{}".format(str(season),str(season+1)))
    if not os.path.exists(data_root_path):
        os.makedirs(data_root_path)
    
    matches_data = os.path.join(data_root_path, "match_{}.csv".format(str(i+1).zfill(2)))
    pd.DataFrame(data=df).to_csv(matches_data)

s.stop()
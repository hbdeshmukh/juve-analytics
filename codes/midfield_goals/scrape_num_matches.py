# -*- coding: utf-8 -*-
"""
Created on Wed Dec  8 11:19:49 2021

This script scrapes the number of matches per season, starting from the
11-12 season and dump it in a csv file

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

# Start server and initialize list to save data

s = Service(executable_path="./chromedriver") # Adjust the path accordingly
s.start()

num_matches = []
season = []
start_year = 11
end_year = 22

for i in range(start_year, end_year):
    # Loop over the web containing data for each season
    year = '20{}-20{}'.format(i, i+1)
    season.append(str(i)+'-'+str(i+1))
    url = "https://fbref.com/en/squads/e0652b02/{}/Juventus-Stats".format(year)
    
    driver = Remote(s.service_url)
    driver.get(url)
    
    # Extract the number of matches from the table
            
    content = driver.page_source
    soup = BeautifulSoup(content, "lxml")
    temp = soup.findAll(attrs={"id": "all_matchlogs"})[0].findAll("tr")
    num_matches.append(len(temp) - 2)
    
    time.sleep(1)
    driver.close()
    
s.stop()

# Dump data to a csv file

data = {'season':season, 'total matches':num_matches}
data_root_path = os.path.abspath("../../data")
matches_data = os.path.join(data_root_path, "matches.csv")
pd.DataFrame(data=data).to_csv(matches_data)
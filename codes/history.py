# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 10:19:05 2021

@author: timot
"""

import requests
import urllib.request
import time
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver import Remote
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import lxml

s = Service(executable_path="./chromedriver")
s.start()
driver = Remote(s.service_url)
# driver = Chrome(service=s)
url = "https://www.whoscored.com/Teams/87/Archive/Italy-Juventus"
driver.get(url)
results = []


select_box = driver.find_element(By.ID,'stageId')
options = [x for x in select_box.find_elements_by_tag_name("option")]

for element in options:
    results.append(element.get_attribute("value"))

results.reverse()


    
# time.sleep(1)
# driver.quit()

driver.close()
s.stop()

urls = []
for i in range(len(results)):
    url_root = "https://www.whoscored.com/Teams/87/Archive/Italy-Juventus?stageId="
    urls.append(url_root + results[i])


players = []
name = []
season = []

def get_data(players, name, season, driver, urls):
    s = Service(executable_path="./chromedriver")
    s.start()
    
    
        
    for url in urls:
        # driver = Chrome(service=s)
        driver = Remote(s.service_url)
        driver.get(url)
        
        content = driver.page_source
        soup = BeautifulSoup(content, "lxml")
        # print(soup)
        
        temp_players = soup.findAll("tr")
        temp_players = temp_players[1:]
        temp_name = []
        temp_positions = []
        
        temp_idx = soup.findAll(attrs={"selected": "selected"})[1].text.strip().index("-")
        temp_season = soup.findAll(attrs={"selected": "selected"})[1].text.strip()[temp_idx+2:]
        
        if temp_season not in season:
            season.append(temp_season)
            init_season = True
        else:
            init_season = False
            
        competition = soup.findAll(attrs={"selected": "selected"})[1].text.strip()[:temp_idx-1]
        
        time.sleep(2)
        
        for player in temp_players:
            temp_name = player.find(attrs={"class": "player-link iconize iconize-icon-left"}).text.strip()
            new_ps = temp_name not in name
            if new_ps:
                players.append({})
                name.append(temp_name)
                metadata = player.findAll(attrs={"class": "player-meta-data"})
                temp_positions = metadata[1].text[3:].strip()
                idx_player = len(players) - 1
                players[idx_player]["Name"] = temp_name
                players[idx_player]["Pos"] = temp_positions
            else:
                idx_player = name.index(temp_name)
            
            if init_season or new_ps:
                players[idx_player][season[-1]] = {}
            
            print(idx_player, season[-1])
            players[idx_player][season[-1]][competition] = {}
            
            temp_apps = player.findAll("td")[4].text.strip()
            if "(" not in temp_apps:
                players[idx_player][season[-1]][competition]["Apps (start)"] = int(temp_apps)
                players[idx_player][season[-1]][competition]["Apps (bench)"] = 0
            else:
                start_idx = temp_apps.index("(")
                end_idx = temp_apps.index(")")
                players[idx_player][season[-1]][competition]["Apps (start)"] = int(temp_apps[:start_idx])
                players[idx_player][season[-1]][competition]["Apps (bench)"] = int(temp_apps[start_idx+1:end_idx])
        
        time.sleep(5)
        driver.close()
        # driver.quit()
    
    
    s.stop()
    
    return players



players = get_data(players, name, season, driver, urls)
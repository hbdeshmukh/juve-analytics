# -*- coding: utf-8 -*-
"""
Created on Thu Dec  9 10:42:54 2021

This script cleans the csv file taken from fbref.com
It removes the last column "matches" that only contain links to detailed
statistics of each match, the first row that contains double table header,
and clean the special characters from the players' names for better parsing

WARNING: ONLY RUN THIS SCRIPT DIRECTLY AFTER DOWNLOADING THE CSV FILE, ALL THE
EXISTING CSV FILES ARE ALREADY CLEAN!

@author: timot
"""

import os
import pandas as pd

# Set data root path and read csv files
filename = "21-22.csv" # Change the filename accordingly
data_root_path = os.path.abspath("../data/general")
filepath = os.path.join(data_root_path, filename)
data = pd.read_csv(filepath, header=1)

# Remove the last column
data.drop(data.columns[-1], axis=1, inplace=True)

# Clean player names
player_names = data['Player'].tolist()
for i in range(len(player_names)):
    player_names[i] = player_names[i][:player_names[i].find("\\")]

data['Player'] = player_names

# Dump the clean dataframe back into the csv file
pd.DataFrame(data=data).to_csv(filepath, index=False)
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 09:21:30 2022

This script scrapes the betting odds data, and use them to simulate the
'expected points' and compare them against the actual points obtained during
the corresponding match.

Data taken from https://www.football-data.co.uk/italym.php

@author: timot
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

## Define the seasons to be analyzed, and relevant data to extract

seasons = np.arange(7,21)
cols = ['HomeTeam', 'AwayTeam', 'FTR', 'B365H', 'B365D', 'B365A']
data_list = []
x_label = []

## Loop over each season

for i in range(len(seasons)):
    # Define the URL for the link to the csv file
    URL = f"https://www.football-data.co.uk/mmz4281/{str(seasons[i]).zfill(2)}{str(seasons[i]+1).zfill(2)}/I1.csv"
    
    # Load and convert the csv file into a dataframe object
    df_temp = pd.read_csv(URL, usecols=cols).dropna()
    
    # Filter only Juventus' matches
    idx_home = df_temp.where(df_temp['HomeTeam'] == 'Juventus').dropna().index
    idx_away = df_temp.where(df_temp['AwayTeam'] == 'Juventus').dropna().index
    idx = idx_home | idx_away
    df_temp = df_temp.loc[idx]
    
    # Convert odds to probability and normalize    
    total_prob = 1/df_temp['B365H'] + 1/df_temp['B365D'] + 1/df_temp['B365A']
    df_temp['ProbH'] = 1/df_temp['B365H'] / total_prob
    df_temp['ProbD'] = 1/df_temp['B365D'] / total_prob
    df_temp['ProbA'] = 1/df_temp['B365A'] / total_prob
    
    # Calculate expected points based on probabilities
    df_temp['XPoints'] = np.zeros(len(df_temp))
    df_temp.loc[idx_home, 'XPoints'] = df_temp['ProbH'][idx_home] * 3  + df_temp['ProbD'][idx_home]
    df_temp.loc[idx_away, 'XPoints'] = df_temp['ProbA'][idx_away] * 3  + df_temp['ProbD'][idx_away]
    
    # Calculate actual points based on actual results
    df_temp['ActPoints'] = np.zeros(len(df_temp))
    df_temp.loc[idx_home, 'ActPoints'] = (df_temp['FTR'][idx_home] == 'H') * 3
    df_temp.loc[idx_away, 'ActPoints'] = (df_temp['FTR'][idx_away] == 'A') * 3
    idx_draw = df_temp.where(df_temp['FTR'] == 'D').dropna().index
    df_temp.loc[idx_draw, 'ActPoints'] = np.ones(len(idx_draw))
    
    # Append data to the list
    data_list.append(df_temp.reset_index(drop=True))
    x_label.append(f'{str(seasons[i]).zfill(2)}/{str(seasons[i]+1).zfill(2)}')
    
## Plot density distribution and evolution

xPoints = np.zeros(len(data_list))
actPoints = np.zeros(len(data_list))
for i in range(len(data_list)):
    xPoints[i] = data_list[i]['XPoints'].sum()
    actPoints[i] = data_list[i]['ActPoints'].sum()
    
plt.figure()
sns.kdeplot(xPoints, label='expected points')
sns.kdeplot(actPoints, label='actual points')
plt.xlabel('Points')
plt.title('Distribution of points per season')
plt.legend()
plt.savefig('points_dist.png')

fig, ax = plt.subplots()
plt.plot(xPoints, label='expected points')
plt.plot(actPoints, label='actual points')
ax.axes.set_xticks(np.arange(0,len(xPoints),2))
ax.set_xticklabels(np.array(x_label)[np.arange(0,len(xPoints),2).astype(int)])
plt.xlabel('Season')
plt.ylabel('Points')
plt.title('Expected and actual points per season')
plt.legend()
plt.savefig('exp_act_points.png')
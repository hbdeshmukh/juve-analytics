# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 10:19:05 2021

This script compiles the goals scored by each position starting from the
season 11-12, focusing on the midfielder

Data taken from https://github.com/hbdeshmukh/juve-analytics/commits?author=spiz006

@author: timot
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Set data root path and read csv files
data_root_path = os.path.abspath("../../data")
players_data = pd.read_csv(os.path.join(data_root_path, "players.csv"))
goals_data = pd.read_csv(os.path.join(data_root_path, "goals.csv"))
matches_data = pd.read_csv(os.path.join(data_root_path, "matches.csv"))

# Initiate dicts for defenders, midfielders, and attackers separately
# The dicts are separated into different seasons, each season into different
# competitions
data = {'d':{}, 'm':{}, 'f':{}}
start_year = 11
end_year = 22
comps = ['Serie A','Coppa Italia','Supercoppa Italiana',
         'UEFA Champions League','UEFA Europa League']

for i in range(start_year, end_year):
    data['d'][str(i)+'-'+str(i+1)] = {}
    data['m'][str(i)+'-'+str(i+1)] = {}
    data['f'][str(i)+'-'+str(i+1)] = {}
    for comp in comps:
        data['d'][str(i)+'-'+str(i+1)][comp] = 0
        data['m'][str(i)+'-'+str(i+1)][comp] = 0
        data['f'][str(i)+'-'+str(i+1)][comp] = 0

# Loop over the goals data and aggregate goals for different positions,
# according to season and competition
for i in range(len(goals_data)):
    temp = goals_data.loc[i]
    if temp['description'] != 'og':
        # Only count goals scored by Juve players
        temp_pos = players_data[players_data['player'] == temp['player']]['position'].item()
        data[temp_pos][temp['season']][temp['competition']] += 1


# PLot midfielder goals divided per competition
serie_a = np.zeros(end_year - start_year)
coppa_italia = np.zeros(end_year - start_year)
supercoppa = np.zeros(end_year - start_year)
ucl = np.zeros(end_year - start_year)
europa = np.zeros(end_year - start_year)

x_label = []
x_plot = 8*np.arange(end_year - start_year)

for i in range(end_year-start_year):
    serie_a[i] = data['m'][str(start_year+i)+'-'+str(start_year+i+1)]['Serie A']
    coppa_italia[i] = data['m'][str(start_year+i)+'-'+str(start_year+i+1)]['Coppa Italia']
    supercoppa[i] = data['m'][str(start_year+i)+'-'+str(start_year+i+1)]['Supercoppa Italiana']
    ucl[i] = data['m'][str(start_year+i)+'-'+str(start_year+i+1)]['UEFA Champions League']
    europa[i] = data['m'][str(start_year+i)+'-'+str(start_year+i+1)]['UEFA Europa League']
    
    x_label.append(str(start_year+i)+'-'+str(start_year+i+1))


fig = plt.figure(figsize=(15,4))
plt.axvspan(-4, 20, facecolor='b', alpha=0.2)
plt.axvspan(20, 60, facecolor='r', alpha=0.2)
plt.axvspan(60, 68, facecolor='g', alpha=0.2)
plt.axvspan(68, 76, facecolor='y', alpha=0.2)
plt.axvspan(76, 84, facecolor='r', alpha=0.2)
plt.bar(x_plot-2, serie_a, width=1, label='Serie A')
plt.bar(x_plot-1, coppa_italia, width=1, label='Coppa Italia')
plt.bar(x_plot, supercoppa, width=1, label='Supercoppa Italiana')
plt.bar(x_plot+1, ucl, width=1, label='UEFA Champions League')
plt.bar(x_plot+2, europa, width=1, label='UEFA Europa League')
plt.xlim([-4, 84])
plt.xticks(x_plot, labels=x_label, rotation='vertical', fontsize=15)
plt.yticks(fontsize=15)
plt.title('Goals scored by midfielders', fontsize=20)
plt.legend()
plt.tight_layout()
plt.savefig('mf_goals_comps.png')

# Plot goals scored by different positions over the years
goals_def = np.zeros(end_year - start_year)
goals_mid = np.zeros(end_year - start_year)
goals_att = np.zeros(end_year - start_year)

for i in range(end_year-start_year):
    goals_def[i] += data['d'][str(start_year+i)+'-'+str(start_year+i+1)]['Serie A'] \
                    + data['d'][str(start_year+i)+'-'+str(start_year+i+1)]['Coppa Italia'] \
                    + data['d'][str(start_year+i)+'-'+str(start_year+i+1)]['Supercoppa Italiana'] \
                    + data['d'][str(start_year+i)+'-'+str(start_year+i+1)]['UEFA Champions League'] \
                    + data['d'][str(start_year+i)+'-'+str(start_year+i+1)]['UEFA Europa League']
    
    goals_mid[i] += data['m'][str(start_year+i)+'-'+str(start_year+i+1)]['Serie A'] \
                    + data['m'][str(start_year+i)+'-'+str(start_year+i+1)]['Coppa Italia'] \
                    + data['m'][str(start_year+i)+'-'+str(start_year+i+1)]['Supercoppa Italiana'] \
                    + data['m'][str(start_year+i)+'-'+str(start_year+i+1)]['UEFA Champions League'] \
                    + data['m'][str(start_year+i)+'-'+str(start_year+i+1)]['UEFA Europa League']
    
    goals_att[i] += data['f'][str(start_year+i)+'-'+str(start_year+i+1)]['Serie A'] \
                    + data['f'][str(start_year+i)+'-'+str(start_year+i+1)]['Coppa Italia'] \
                    + data['f'][str(start_year+i)+'-'+str(start_year+i+1)]['Supercoppa Italiana'] \
                    + data['f'][str(start_year+i)+'-'+str(start_year+i+1)]['UEFA Champions League'] \
                    + data['f'][str(start_year+i)+'-'+str(start_year+i+1)]['UEFA Europa League']

fig, ax = plt.subplots(2,1,figsize=(15,8))
ax[0].axvspan(-4, 20, facecolor='b', alpha=0.2)
ax[0].axvspan(20, 60, facecolor='r', alpha=0.2)
ax[0].axvspan(60, 68, facecolor='g', alpha=0.2)
ax[0].axvspan(68, 76, facecolor='y', alpha=0.2)
ax[0].axvspan(76, 84, facecolor='r', alpha=0.2)
ax[0].plot(x_plot, goals_def, label='Defender')
ax[0].plot(x_plot, goals_mid, label='Midfielder')
ax[0].plot(x_plot, goals_att, label='Forward')
ax[0].set_xlim([-4, 84])
ax[0].set_xticks([])
# ax[0].set_xticklabels(x_label, rotation='vertical', fontsize=15)
ax[0].set_yticks([20,40,60,80])
ax[0].set_yticklabels([20,40,60,80],fontsize=15)
ax[0].set_title('Goals scored by different positions', fontsize=20)
ax[0].legend()

# Plot goals per matches scored by different positions over the years
gpm_def = goals_def/matches_data['total matches'].to_numpy()
gpm_mid = goals_mid/matches_data['total matches'].to_numpy()
gpm_att = goals_att/matches_data['total matches'].to_numpy()

ax[1].axvspan(-4, 20, facecolor='b', alpha=0.2)
ax[1].axvspan(20, 60, facecolor='r', alpha=0.2)
ax[1].axvspan(60, 68, facecolor='g', alpha=0.2)
ax[1].axvspan(68, 76, facecolor='y', alpha=0.2)
ax[1].axvspan(76, 84, facecolor='r', alpha=0.2)
ax[1].plot(x_plot, gpm_def, label='Defender')
ax[1].plot(x_plot, gpm_mid, label='Midfielder')
ax[1].plot(x_plot, gpm_att, label='Forward')
ax[1].set_xlim([-4, 84])
ax[1].set_xticks(x_plot)
ax[1].set_xticklabels(x_label, rotation='vertical', fontsize=15)
ax[1].set_yticks([0, 0.5, 1.0, 1.5, 2.0])
ax[1].set_yticklabels([0, 0.5, 1.0, 1.5, 2.0],fontsize=15)
ax[1].set_title('Goals per match scored by different positions', fontsize=20)
ax[1].legend()
plt.tight_layout()
plt.savefig('mf_df_fw_goals.png')

# Load  and plot goals and xG of every midfielder from the season 17-18 and 20-21
data_now = pd.read_csv(os.path.join(data_root_path, "general\\20-21.csv"))
data_now = data_now.loc[data_now['Pos'].str.contains("M", case=False)]
data_now = data_now.loc[~data_now['xG'].isnull()]
xg_now = data_now['xG'].to_numpy()
goals_now = data_now['Gls'].to_numpy()
idx = np.argsort(xg_now)
xg_now = xg_now[idx]
goals_now = goals_now[idx]
# Linear regression
temp = np.poly1d(np.polyfit(xg_now, goals_now, 1))
line_now = temp(xg_now)

data_old = pd.read_csv(os.path.join(data_root_path, "general\\17-18.csv"))
data_old = data_old.loc[data_old['Pos'].str.contains("M", case=False)]
data_old = data_old.loc[~data_old['xG'].isnull()]
xg_old = data_old['xG'].to_numpy()
goals_old = data_old['Gls'].to_numpy()
idx = np.argsort(xg_old)
xg_old = xg_old[idx]
goals_old = goals_old[idx]
# Linear regression
temp = np.poly1d(np.polyfit(xg_old, goals_old, 1))
line_old = temp(xg_old)

fig = plt.figure(figsize=(5,5))
plt.scatter(xg_old, goals_old, label='17-18')
plt.scatter(xg_now, goals_now, label='20-21')
plt.plot(xg_old, line_old)
plt.plot(xg_now, line_now)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.xlabel('xG',fontsize=15)
plt.ylabel('Goals',fontsize=15)
plt.title('xG vs goals scored', fontsize=20)
plt.legend()
plt.tight_layout()
plt.savefig('mf_xg_goals.png')
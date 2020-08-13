import requests
import pandas as pd
import json
import numpy as np

# getting raw data from fpl API
url_1 = 'https://fantasy.premierleague.com/api/bootstrap-static/'
url_2 = 'https://fantasy.premierleague.com/api/fixtures/'
r_1 = requests.get(url_1)
r_2 = requests.get(url_2)
json_1 = r_1.json()
json_2 = r_2.json()
data_path = 'data\\'

# convert received jsons to csv
events_df = pd.DataFrame(json_1['events'])
game_settings_df = pd.DataFrame([json_1['game_settings']])
phases_df = pd.DataFrame(json_1['phases'])
teams_df = pd.DataFrame(json_1['teams'])
total_players_df = pd.DataFrame([json_1['total_players']])
elements_df = pd.DataFrame(json_1['elements'])
element_stats_df = pd.DataFrame(json_1['element_stats'])
element_types_df = pd.DataFrame(json_1['element_types'])
fixtures_df = pd.DataFrame(json_2)

# saving data to csv files
events_df.to_csv(data_path + 'events.csv')
game_settings_df.to_csv(data_path + 'game_settings.csv')
phases_df.to_csv(data_path + 'phases.csv')
teams_df.to_csv(data_path + 'teams.csv')
total_players_df.to_csv(data_path + 'total_players.csv')
elements_df.to_csv(data_path + 'elements.csv')
element_stats_df.to_csv(data_path + 'element_stats.csv')
element_types_df.to_csv(data_path + 'element_types.csv')
fixtures_df.to_csv(data_path + 'fixtures.csv')

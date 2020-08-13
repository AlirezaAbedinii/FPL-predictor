import requests
import pandas as pd
import numpy as np

url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
r = requests.get(url)
json = r.json()
data_path = 'data\\'

events_df = pd.DataFrame(json['events'])
#game_settings_df = pd.DataFrame(json['game_settings'])
phases_df = pd.DataFrame(json['phases'])
teams_df = pd.DataFrame(json['teams'])
#total_players_df = pd.DataFrame(json['total_players'])
elements_df = pd.DataFrame(json['elements'])
element_stats_df = pd.DataFrame(json['element_stats'])
element_types_df = pd.DataFrame(json['element_types'])

events_df.to_csv(data_path + 'events.csv')
#game_settings_df.to_csv(data_path + 'game_settings.csv')
phases_df.to_csv(data_path + 'phases.csv')
teams_df.to_csv(data_path + 'teams.csv')
#total_players_df.to_csv(data_path + 'total_players.csv')
elements_df.to_csv(data_path + 'elements.csv')
element_stats_df.to_csv(data_path + 'element_stats.csv')
element_types_df.to_csv(data_path + 'element_types.csv')

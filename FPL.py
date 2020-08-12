import requests
import pandas as pd
import numpy as np

url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
r = requests.get(url)
json = r.json()
print(json.keys())

events_df = pd.DataFrame(json['events'])
#game_settings_df = pd.DataFrame(json['game_settings']) has error
phases_df = pd.DataFrame(json['phases'])
teams_df = pd.DataFrame(json['teams'])
#total_players_df = pd.DataFrame(json['total_players']) has error
elements_df = pd.DataFrame(json['elements'])
element_stats_df = pd.DataFrame(json['element_stats'])
elements_types_df = pd.DataFrame(json['element_types'])

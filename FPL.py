import requests
import pandas as pd
import numpy as np

url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
r = requests.get(url)
json = r.json()
print(json.keys())

events_df = pd.DataFrame(json['events'])
#game_settings_df = pd.DataFrame(json['game_settings'])
phases_df = pd.DataFrame(json['phases'])
teams_df = pd.DataFrame(json['teams'])
#total_players_df = pd.DataFrame(json['total_players']) has error
elements_df = pd.DataFrame(json['elements'])
element_stats_df = pd.DataFrame(json['element_stats'])
elements_types_df = pd.DataFrame(json['element_types'])

slim_elements_df = elements_df[['first_name','second_name','team','element_type','selected_by_percent','now_cost','bonus','minutes','transfers_in','value_season','total_points']]
slim_elements_df['position'] = slim_elements_df.element_type.map(elements_types_df.set_index('id').singular_name)
slim_elements_df['team'] = slim_elements_df.team.map(teams_df.set_index('id').name)
slim_elements_df['value'] = slim_elements_df.value_season.astype(float)
slim_elements_df['bonus_percent'] = slim_elements_df.bonus.astype(float)/slim_elements_df.total_points.astype(float)
#print(slim_elements_df.sort_values('value',ascending=False).head(100))

#print((slim_elements_df[slim_elements_df.bonus_percent.gt(0)].pivot_table(index='position',values='bonus_percent',aggfunc=np.mean).reset_index()).sort_values('bonus_percent', ascending=False))
print(slim_elements_df[slim_elements_df.total_points.gt(99)].sort_values('bonus_percent', ascending=False))
print("kos")
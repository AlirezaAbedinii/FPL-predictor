import pandas as pd
import numpy as np

data_path = 'data\\'

events_df = pd.read_csv(data_path + 'events.csv')
#game_settings_df = pd.read_csv('game_settings.csv')
phases_df = pd.read_csv(data_path + 'phases.csv')
teams_df = pd.read_csv(data_path + 'teams.csv')
#total_players_df = pd.read_csv('total_players.csv')
elements_df = pd.read_csv(data_path + 'elements.csv')
element_stats_df = pd.read_csv(data_path + 'element_stats.csv')
element_types_df = pd.read_csv(data_path + 'element_types.csv')


slim_elements_df = elements_df[['first_name','second_name','team','element_type','selected_by_percent','now_cost','bonus','minutes','transfers_in','value_season','total_points']]
slim_elements_df['position'] = slim_elements_df.element_type.map(element_types_df.set_index('id').singular_name)
slim_elements_df['team'] = slim_elements_df.team.map(teams_df.set_index('id').name)
slim_elements_df['value'] = slim_elements_df.value_season.astype(float)
slim_elements_df['bonus_percent'] = slim_elements_df.bonus.astype(float)/slim_elements_df.total_points.astype(float)
#print(slim_elements_df.sort_values('value',ascending=False).head(100))

#print((slim_elements_df[slim_elements_df.bonus_percent.gt(0)].pivot_table(index='position',values='bonus_percent',aggfunc=np.mean).reset_index()).sort_values('bonus_percent', ascending=False))
print(slim_elements_df.loc[slim_elements_df.total_points>=100].sort_values('bonus_percent', ascending=False))
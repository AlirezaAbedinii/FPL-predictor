import pandas as pd
import json
import numpy as np


class Stat:
    def __init__(self, raw_string):
        json_string = raw_string.replace('\'', '\"')
        stat_json = json.loads(json_string)

        for js in stat_json:
            # print(js['identifier'])
            del js['identifier']

        self.goals_scored = stat_json[0]
        self.assists = stat_json[1]
        self.own_goals = stat_json[2]
        self.penalties_saved = stat_json[3]
        self.penalties_missed = stat_json[4]
        self.yellow_cards = stat_json[5]
        self.red_cards = stat_json[6]
        self.saves = stat_json[7]
        self.bonus = stat_json[8]
        self.bps = stat_json[9]

    def __str__(self):
        results = 'goals scored' + str(self.goals_scored) + 'assists' + str(self.assists)
        results += 'own goals' + str(self.own_goals) + 'penalties saved' + str(self.penalties_saved)
        results += 'penalties missed' + str(self.penalties_missed) + 'yellow cards' + str(self.yellow_cards)
        results += 'red cards' + str(self.red_cards) + 'saves' + str(self.saves)
        results += 'bonus' + str(self.bonus) + 'bps' + str(self.bps)
        return results


def player_type(player_name):
    return elements_df.loc[elements_df['first_name'] + '_' + elements_df['second_name'] + '_' + elements_df['id'].apply(
        str) == player_name].element_type.tolist()[0]

def player_team(player_name):
    return elements_df.loc[elements_df['first_name'] + '_' + elements_df['second_name'] + '_' + elements_df['id'].apply(
        str) == player_name].team.tolist()[0]


# this method returns player id given his second_name
def name_to_id(player_second_name):
    ids = elements_df.loc[elements_df.second_name == player_second_name].id.tolist()
    if (len(ids) == 1):
        return ids[0]
    return ids


def player_data(player_id):
    return elements_df.loc[elements_df.id == player_id]


# this method returns home goals scored by a player given his id
def home_goals(player_id):
    h = 0
    for stat in classified_stats:
        for element in stat.goals_scored['h']:
            if (element['element'] == player_id):
                h += element['value']
    return h


# this method returns away goals scored by a player given his id

def away_goals(player_id):
    a = 0
    for stat in classified_stats:
        for element in stat.goals_scored['a']:
            if (element['element'] == player_id):
                a += element['value']
    return a


# this method returns home assists provided by a player given his id
def home_assists(player_id):
    h = 0
    for stat in classified_stats:
        for element in stat.assists['h']:
            if (element['element'] == player_id):
                h += element['value']
    return h


# this method returns away assists provided by a player given his id
def away_assists(player_id):
    a = 0
    for stat in classified_stats:
        for element in stat.assists['a']:
            if (element['element'] == player_id):
                a += element['value']
    return a

data_path = 'data\\'
history_path = 'history\\'

events_df = pd.read_csv(data_path + 'events.csv')
# game_settings_df = pd.read_csv('game_settings.csv')
phases_df = pd.read_csv(data_path + 'phases.csv')
teams_df = pd.read_csv(data_path + 'teams.csv')
# total_players_df = pd.read_csv('total_players.csv')
elements_df = pd.read_csv(data_path + 'elements.csv')
element_stats_df = pd.read_csv(data_path + 'element_stats.csv')
element_types_df = pd.read_csv(data_path + 'element_types.csv')
fixtures_df = pd.read_csv(data_path + 'fixtures.csv')
gw_df = pd.read_csv('merged_gw.csv')
# history_df = pd.read_csv(data_path + history_path + )

classified_stats = []
for i in range(len(fixtures_df)):
    stat_obj = Stat(str(fixtures_df.iloc[i].stats))
    classified_stats.append(stat_obj)

# replacing raw stats with serialized Stat class
fixtures_df.stats = classified_stats

# slim_elements_df = elements_df[['first_name','second_name','team','element_type','selected_by_percent','now_cost','bonus','minutes','transfers_in','value_season','total_points']]
# elements_df['position'] = elements_df.element_type.map(element_types_df.set_index('id').singular_name) #replace position name with position id
# del elements_df['element_type']
#elements_df['team'] = elements_df.team.map(teams_df.set_index('id').name)  # replace team name with team id
# print(elements_df[['first_name','second_name','position','team']])
elements_df['bonus_percent'] = elements_df.bonus.astype(float) / elements_df.total_points.astype(float)
# print(elements_df.sort_values())


elements_df['home_goals'] = elements_df['id'].apply(lambda x: home_goals(x))  # add home_goals column to elements
elements_df['away_goals'] = elements_df['id'].apply(lambda x: away_goals(x))  # add away_goals column to elements
elements_df['home_assists'] = elements_df['id'].apply(lambda x: home_assists(x))  # add home_assists column to elements
elements_df['away_assists'] = elements_df['id'].apply(lambda x: away_assists(x))  # add away_assists column to elements
# pd.set_option('display.max_columns', None) #show all columns when printing
pd.set_option('display.max_rows', None)  # show all rows when printing

# collect cumulative data and save to csv
gw_df['GW'] = gw_df['GW'].apply(lambda x: x if x <= 29 else x - 9)
gw_df = gw_df.loc[gw_df.minutes != 0]

no_zero_df = gw_df.loc[gw_df.minutes > 0].groupby(['name', 'GW','fixture']).sum().reset_index()
no_zero_df.to_csv('no_zero.csv', index=False)

cumulative_df = no_zero_df[['name', 'GW', 'fixture', 'goals_scored', 'assists', 'bonus', 'bps', 'red_cards', 'penalties_saved', 'penalties_missed',
        'clean_sheets','saves', 'goals_conceded', 'yellow_cards', 'minutes', 'total_points']]

cumulative_df = cumulative_df.groupby(['name','GW','fixture']).sum().groupby(level=0).cumsum().reset_index()
cumulative_df['total_points'] = cumulative_df['total_points'] - no_zero_df['total_points']
cumulative_df['position'] = cumulative_df['name'].apply(lambda x: player_type(x))
cumulative_df['was_home'] = no_zero_df['was_home']

# adding difficulty file
# difficulty_df1 = fixtures_df[['event', 'team_h', 'team_a', 'team_h_difficulty']]
# difficulty_df1 = difficulty_df1.rename(columns={'event': 'GW', 'team_h': 'team_id', 'team_a': 'opponent_id', 'team_h_difficulty': 'difficulty'})
#
# difficulty_df2 = fixtures_df[['event', 'team_a', 'team_h', 'team_a_difficulty']]
# difficulty_df2 = difficulty_df2.rename(columns={'event': 'GW', 'team_a': 'team_id', 'team_h': 'opponent_id', 'team_a_difficulty': 'difficulty'})
#
# difficulty_df = difficulty_df1.append(difficulty_df2, ignore_index=True)
#
# difficulty_df['GW'] = difficulty_df['GW'].apply(lambda x: x if x <= 29 else x - 9)
difficulty_df = fixtures_df[['id', 'team_h_difficulty', 'team_a_difficulty']]
difficulty_df.to_csv('difficulties.csv', index=False)
#
cumulative_df = cumulative_df.merge(difficulty_df,  how='left', left_on='fixture', right_on = 'id')
cumulative_df['difficulty'] = cumulative_df['team_h_difficulty']*cumulative_df['was_home'] + cumulative_df['team_a_difficulty']*(1 - cumulative_df['was_home'])
cumulative_df.to_csv('cumulative_gw_2.csv', index=False)

total_points_df = no_zero_df[['name', 'GW', 'fixture', 'total_points']]
total_points_df = total_points_df.groupby(['name','GW', 'fixture']).sum().reset_index()
total_points_df['position'] = total_points_df['name'].apply(lambda x: player_type(x))
total_points_df.to_csv('total_points_gw_2.csv', index=False)

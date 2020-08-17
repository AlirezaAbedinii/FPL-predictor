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


def calculate_form(number_of_games, df):
    forms_array = []
    for i in range(len(df)):
        name = df.iloc[i]['name']
        points = 0.0
        past_games = min(number_of_games, df.iloc[i]['GW'] - 1)
        counter = 1
        while counter <= past_games and i - counter >= 0:
            if df.iloc[i - counter]['GW'] >= int(df.iloc[i]['GW']) - past_games:
                if df.iloc[i-counter]['name'] == name:
                    points += df.iloc[i - counter]['points']
            counter += 1

        if past_games == 0:
            forms_array.append(0)
        else:
            forms_array.append(points / past_games)

    result = pd.DataFrame(forms_array)
    return result



season = '2018'
data_path = 'data\\' + season + '\\'
learning_data_path = 'mh_learning_data\\' + season + '\\'
temp_data_path = learning_data_path + 'temps\\'

elements_df = pd.read_csv(data_path + 'elements.csv')
fixtures_df = pd.read_csv(data_path + 'fixtures.csv')
print(temp_data_path + 'merged_gw.csv')
gw_df = pd.read_csv(temp_data_path + 'merged_gw.csv', encoding='latin')
gw_df = gw_df.loc[gw_df.minutes != 0]
# classified_stats = []
# for i in range(len(fixtures_df)):
#     stat_obj = Stat(str(fixtures_df.iloc[i].stats))
#     classified_stats.append(stat_obj)
#
# # replacing raw stats with serialized Stat class
# fixtures_df.stats = classified_stats

# pd.set_option('display.max_columns', None) #show all columns when printing
pd.set_option('display.max_rows', None)  # show all rows when printing

# collect cumulative data and save to csv
#gw_df['GW'] = gw_df['GW'].apply(lambda x: x if x <= 29 else x - 9)

#cumulative goals scored by teams_per_week
home_scores_df = fixtures_df[['event','team_h','team_h_score']].rename(columns={'event': 'GW', 'team_h': 'team'}).groupby(['team','GW']).sum().reset_index()
away_scores_df = fixtures_df[['event','team_a','team_a_score']].rename(columns={'event': 'GW', 'team_a': 'team'}).groupby(['team','GW']).sum().reset_index()
scores_df = home_scores_df.append(away_scores_df, ignore_index=True)
scores_df = scores_df.groupby(['team','GW']).sum().reset_index()
scores_df['week_goals'] = scores_df['team_a_score'] + scores_df['team_h_score']
scores_df['opponent_goals'] = scores_df['team_h_score'] + scores_df['team_a_score']
scores_df = scores_df.groupby(['team','GW','week_goals']).sum().groupby(level=0).cumsum().reset_index()
#scores_df['GW'] = scores_df['GW'].apply(lambda x: x if x <= 29 else x - 9)
scores_df['opponent_goals'] -= scores_df['week_goals']
scores_df = scores_df[['team','GW','opponent_goals']]
scores_df.to_csv(temp_data_path + 'scores.csv', index=False)

#cumulative goals conceded by teams_per_week
home_concedes_df = fixtures_df[['event','team_h','team_a_score']].rename(columns={'event': 'GW', 'team_h': 'team'}).groupby(['team','GW']).sum().reset_index()
away_concedes_df = fixtures_df[['event','team_a','team_h_score']].rename(columns={'event': 'GW', 'team_a': 'team'}).groupby(['team','GW']).sum().reset_index()
concedes_df = home_concedes_df.append(away_concedes_df, ignore_index=True)
concedes_df = concedes_df.groupby(['team','GW']).sum().reset_index()
concedes_df['week_goals'] = concedes_df['team_a_score'] + concedes_df['team_h_score']
concedes_df['opponent_conceded'] = concedes_df['team_h_score'] + concedes_df['team_a_score']
concedes_df = concedes_df.groupby(['team','GW','week_goals']).sum().groupby(level=0).cumsum().reset_index()
#concedes_df['GW'] = concedes_df['GW'].apply(lambda x: x if x <= 29 else x - 9)
concedes_df['opponent_conceded'] -= concedes_df['week_goals']
concedes_df = concedes_df[['team','GW','opponent_conceded']]
concedes_df.to_csv(temp_data_path + 'concedes.csv', index=False)


no_zero_df = gw_df.loc[gw_df.minutes > 0].groupby(['name', 'GW','fixture']).sum().reset_index()
del no_zero_df['id']
no_zero_df.to_csv(temp_data_path + 'no_zero.csv', index=False)
cumulative_df = no_zero_df[['name', 'GW', 'fixture','opponent_team', 'goals_scored', 'assists', 'bonus', 'bps', 'red_cards', 'penalties_saved', 'penalties_missed',
        'clean_sheets','saves', 'goals_conceded', 'yellow_cards', 'minutes', 'total_points']]
cumulative_df = cumulative_df.merge(fixtures_df[['id','team_a_score','team_h_score']],  how='left', left_on='fixture', right_on = 'id')
cumulative_df = cumulative_df.groupby(['name','GW','fixture', 'opponent_team']).sum().groupby(level=0).cumsum().reset_index()
cumulative_df['total_points'] = cumulative_df['total_points'] - no_zero_df['total_points']
cumulative_df['position'] = cumulative_df['name'].apply(lambda x: player_type(x))
cumulative_df['was_home'] = no_zero_df['was_home']

difficulty_df = fixtures_df[['id', 'team_h_difficulty', 'team_a_difficulty']]
difficulty_df.to_csv(temp_data_path + 'difficulties.csv', index=False)
#
cumulative_df = cumulative_df.merge(difficulty_df,  how='left', left_on='fixture', right_on = 'id')
cumulative_df = cumulative_df.merge(scores_df, how='left', left_on=['GW','opponent_team'], right_on=['GW', 'team'])
cumulative_df = cumulative_df.merge(concedes_df, how='left', left_on=['GW','opponent_team'], right_on=['GW', 'team'])
cumulative_df['difficulty'] = cumulative_df['team_h_difficulty']*cumulative_df['was_home'] + cumulative_df['team_a_difficulty']*(1 - cumulative_df['was_home'])
del cumulative_df['id_x']
del cumulative_df['id_y']
del cumulative_df['team_x']
del cumulative_df['team_y']

cumulative_df['opponent_goals'] = cumulative_df['opponent_goals'] / abs(cumulative_df['GW'] - 1.00001)
cumulative_df['opponent_conceded'] = cumulative_df['opponent_conceded'] / abs(cumulative_df['GW'] - 1.00001)

total_points_df = no_zero_df[['name', 'GW', 'fixture', 'total_points']]
total_points_df = total_points_df.groupby(['name','GW', 'fixture']).sum().reset_index()
total_points_df['position'] = total_points_df['name'].apply(lambda x: player_type(x))
total_points_df.to_csv(temp_data_path + 'total_points_gw_2.csv', index=False)

# adding form
form_df = cumulative_df[['name', 'GW']]  # = calculate_form(4)
form_df['points'] = total_points_df['total_points']
form_df['form'] = calculate_form(4, form_df)
form_df.to_csv(temp_data_path + 'form.csv', index=False)
cumulative_df['form'] = form_df['form']

cumulative_df.to_csv(temp_data_path + 'cumulative_gw_2.csv', index=False)
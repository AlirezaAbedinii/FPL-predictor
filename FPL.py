import pandas as pd
import json
import numpy as np


class Stat:
    def __init__(self, raw_string):
        json_string = raw_string.replace('\'', '\"')
        stat_json = json.loads(json_string)

        for js in stat_json:
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

data_path = 'data\\'

events_df = pd.read_csv(data_path + 'events.csv')
#game_settings_df = pd.read_csv('game_settings.csv')
phases_df = pd.read_csv(data_path + 'phases.csv')
teams_df = pd.read_csv(data_path + 'teams.csv')
#total_players_df = pd.read_csv('total_players.csv')
elements_df = pd.read_csv(data_path + 'elements.csv')
element_stats_df = pd.read_csv(data_path + 'element_stats.csv')
element_types_df = pd.read_csv(data_path + 'element_types.csv')
fixtures_df = pd.read_csv(data_path + 'fixtures.csv')


classified_stats = []
for i in range(len(fixtures_df)):
    stat_obj = Stat(str(fixtures_df.iloc[i].stats))
    classified_stats.append(stat_obj)


# replacing raw stats with serialized Stat class
fixtures_df.stats = classified_stats



#slim_elements_df = elements_df[['first_name','second_name','team','element_type','selected_by_percent','now_cost','bonus','minutes','transfers_in','value_season','total_points']]
# elements_df['position'] = elements_df.element_type.map(element_types_df.set_index('id').singular_name)
# elements_df['team'] = elements_df.team.map(teams_df.set_index('id').name)
# elements_df['value'] = elements_df.value_season.astype(float)
elements_df['bonus_percent'] = elements_df.bonus.astype(float)/elements_df.total_points.astype(float)

#print((slim_elements_df[slim_elements_df.bonus_percent.gt(0)].pivot_table(index='position',values='bonus_percent',aggfunc=np.mean).reset_index()).sort_values('bonus_percent', ascending=False))
print((elements_df.loc[elements_df.total_points>=100].sort_values('bonus_percent', ascending=False))[['first_name', 'second_name', 'bonus_percent']])

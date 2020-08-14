import requests
import pandas as pd
import numpy as np
import os

url = 'https://fantasy.premierleague.com/api/entry/{}/history/'
url2 = 'https://fantasy.premierleague.com/api/element-summary/{}/'

history_path = 'history\\'
data_path = 'data\\'

elements_df = pd.read_csv(data_path + 'elements.csv')
player_ids = elements_df.id.tolist()

for id in player_ids:
    print(id)
    r = requests.get(url2.format(id))
    json = r.json()
    history_past_df = json['history_past']
    for season in history_past_df:
        season_name = season['season_name']
        season_name = season_name.replace('/', '-')
        del season['season_name']
        season_df = pd.DataFrame.from_dict(season, orient='index').transpose()
        header = not os.path.exists(data_path + history_path + season_name + '.csv')
        season_df.to_csv(data_path + history_path + season_name + '.csv', mode='a', header=header, index=False)
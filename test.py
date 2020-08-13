import requests
import pandas as pd
import numpy as np




url = 'https://fantasy.premierleague.com/api/fixtures/'
r = requests.get(url)
json = r.json()
data_path = 'data\\'

fixtures_df = pd.DataFrame(json)
fixtures_df.to_csv(data_path + 'fixtures.csv')
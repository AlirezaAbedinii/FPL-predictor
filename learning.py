import pandas as pd


# first learning
def make_input_output1():
    cumulative_gw_df = pd.read_csv('cumulative_gw.csv')
    need_data = cumulative_gw_df[['name', 'goals_scored', 'assists', 'clean_sheets', 'minutes']]
    total_data = need_data.to_csv(learning_path + 'header.csv', index=False)
    newFile = need_data.to_csv(learning_path + 'first_input.csv', index=False, header=False)


data_path = 'data\\'
learning_path = 'learning_data\\'

make_input_output1()

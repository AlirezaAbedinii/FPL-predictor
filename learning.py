import pandas as pd


# first learning
def make_input1():
    cumulative_gw_df = pd.read_csv('cumulative_gw.csv')
    need_data = cumulative_gw_df[['name', 'goals_scored', 'assists', 'clean_sheets', 'minutes']]
    total_data = need_data.to_csv(learning_path + 'header.csv', index=False)
    newFile = need_data.to_csv(learning_path + 'first_input.csv', index=False, header=False)

    out_df = pd.read_csv('total_points_gw.csv')
    out_file = out_df['total_points'].to_csv(learning_path + 'first_output.csv', index=False, header=False)


def make_output1():
    out_df = pd.read_csv('total_points_gw.csv')
    out_file = out_df['total_points'].to_csv(learning_path + 'first_output.csv', index=False, header=False)


data_path = 'data\\'
learning_path = 'learning_data\\'

# make_input1()
make_output1()

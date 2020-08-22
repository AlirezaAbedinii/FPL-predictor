from builtins import float
from sklearn.metrics import mean_squared_error
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeRegressor
import matplotlib.pyplot as plt

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


def learner(position, gw=38, mode='mixed'):
    x_df = pd.read_csv(data_path + seasons[0] + '\\x.csv')
    y_df = pd.read_csv(data_path + seasons[0] + '\\y.csv')
    necessary_data = data_per_position[position]
    if mode == 'mixed':
        x_df = x_df.append(pd.read_csv(data_path + seasons[1] + '\\x.csv'), ignore_index=True)
        y_df = y_df.append(pd.read_csv(data_path + seasons[1] + '\\y.csv'), ignore_index=True)
    else:
        x2_df = pd.read_csv(data_path + seasons[1] + '\\x.csv')
        y2_df = pd.read_csv(data_path + seasons[1] + '\\y.csv')
        x2_df = x2_df.loc[x2_df['position'] == position]  # select position
        y2_df = y2_df.loc[y2_df['position'] == position]  # select position
        x2_df = x2_df.loc[x2_df['GW'] <= gw]
        y2_df = y2_df.loc[y2_df['GW'] <= gw]
        x2_df = x2_df[necessary_data]
        y2_df = y2_df['total_points']

    x_df = x_df.loc[x_df['position'] == position]  # select position
    y_df = y_df.loc[y_df['position'] == position]  # select position

    x_df = x_df[necessary_data]
    y_df = y_df['total_points']

    for feature in necessary_data:
        x_df[feature] = (x_df[feature] - x_df[feature].min()) / x_df[feature].std()
        x_df[feature] = x_df[feature].replace(np.inf, 0).fillna(0)
        if mode != 'mixed':
            x2_df[feature] = (x2_df[feature] - x2_df[feature].min()) / x2_df[feature].std()
            x2_df[feature] = x2_df[feature].replace(np.inf, 0).fillna(0)

    x = x_df.to_numpy()
    y = y_df.to_numpy().reshape(-1)

    x = x.astype(float)
    y = y.astype(float)

    if mode == 'mixed':
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, shuffle=True)
    else:
        x2 = x2_df.to_numpy()
        y2 = y2_df.to_numpy().reshape(-1)
        x_train = x.astype(float)
        y_train = y.astype(float)
        x_test = x2.astype(float)
        y_test = y2.astype(float)

    if position > 1:
        regressor = MLPRegressor(hidden_layer_sizes=(100,100), solver='adam', activation='logistic', max_iter=100000,
                                 learning_rate_init=0.001).fit(x_train, y_train)
    else:
        regressor = MLPRegressor(hidden_layer_sizes=(200, 200), solver='adam', activation='logistic', max_iter=100000,
                                 learning_rate_init=0.0001, learning_rate='invscaling').fit(x_train, y_train)

    #output = regressor.predict(x_test)
    output = regressor.predict(x_train)
    y_test = y_train

    difference = abs(output - y_test)
    print('VARIANCE = ' + str(np.var(difference)))
    squared_difference = (output - y_test) ** 2
    mse = squared_difference.mean()
    print('MSE = ' + str(mse))
    non_blank_performance(y_test, output, 6, 100)
    df = pd.DataFrame({'Actual': y_test.flatten(), 'Predicted': output.flatten()})
    plt.scatter(y_test, output, color='gray', alpha=0.5)
    plt.show()


def non_blank_performance(real, predicted, threshold1, threshold2):
    real_np = np.array(real)
    predicted_np = np.array(predicted)
    perfect = 0.0
    good = 0.0
    normal = 0.0
    bad = 0.0
    total = 0.0
    difference = abs(real - predicted)
    for i in range(len(real_np)):
        if threshold1 < real[i] < threshold2:
            if difference[i] < 0.5:
                perfect += 1
            elif difference[i] < 2:
                good += 1
            elif difference[i] < 4:
                normal += 1
            else:
                bad += 1
            total += 1
    result = 'perfect:', str(perfect / total), 'good:', str(good / total), 'normal:', str(normal / total), 'bad:', str(
        bad / total)
    print(result)


def pie_chart(real, predicted):
    pass


seasons = ['2018', '2019']
data_path = 'mh_learning_data\\'
data_per_position = dict()
data_per_position[4] = ['GW', 'goals_scored', 'assists', 'opponent_conceded', 'bonus', 'bps', 'form', 'total_points',
                        'was_home', 'minutes', 'yellow_cards', 'red_cards', 'difficulty']
data_per_position[3] = ['opponent_conceded', 'goals_scored', 'assists', 'bonus', 'form', 'bps', 'total_points',
                        'was_home', 'minutes', 'yellow_cards', 'red_cards', 'clean_sheets', 'difficulty']
data_per_position[2] = ['GW', 'opponent_goals', 'goals_scored', 'assists', 'bonus', 'form', 'total_points', 'was_home',
                        'minutes', 'yellow_cards', 'red_cards', 'goals_conceded', 'clean_sheets', 'difficulty']
data_per_position[1] = ['GW', 'opponent_goals', 'bonus', 'minutes', 'bps', 'form', 'total_points', 'saves',
                        'goals_conceded', 'was_home', 'clean_sheets', 'yellow_cards', 'red_cards', 'penalties_saved',
                        'difficulty']

# mode = 'mixed' or 'split'
learner(2, mode='mixed', gw=38)

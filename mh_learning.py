from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np


def learner(position):

    x_df = pd.read_csv(data_path + 'cumulative_gw_2.csv')
    y_df = pd.read_csv(data_path + 'total_points_gw_2.csv')
    x_df = x_df.loc[x_df['position'] == position]  # select position
    y_df = y_df.loc[y_df['position'] == position]  # select position

    necessary_data = data_per_position[position]
    x_df = x_df[necessary_data]
    print(x_df)
    y_df = y_df['total_points']
    x_df['was_home'] = x_df['was_home'].apply(lambda x: 1 if x == True else 0)
    x_df['minutes']/=90.0

    x = x_df.to_numpy()
    y = y_df.to_numpy().reshape(-1)

    x = x.astype(float)
    y = y.astype(float)

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

    regressor = MLPRegressor(hidden_layer_sizes=(5, 10, 5), activation='logistic', max_iter=100000,
                             learning_rate_init=0.001).fit(x_train, y_train)

    output = regressor.predict(x_test)

    mse = ((output - y_test) ** 2).mean()
    print('MSE = ' + str(mse))
    non_blank_performance(y_test, output, 6)


def non_blank_performance(real, predicted, threshold):
    real_np = np.array(real)
    predicted_np = np.array(predicted)
    good = 0.0
    normal = 0.0
    bad = 0.0
    total = 0.0
    difference = abs(real - predicted)
    for i in range(len(real_np)):
        if real[i] > threshold:
            if difference[i] < 2:
                good +=1
            elif difference[i] < 4:
                normal += 1
            else:
                bad += 1
            total += 1
    result = 'good:', str(good/total), 'normal:', str(normal/total), 'bad:', str(bad/total)
    print(result)


data_path = 'mh_learning_data\\'
data_per_position = dict()
data_per_position[4] = ['goals_scored', 'assists', 'bonus', 'total_points', 'was_home', 'minutes', 'yellow_cards']
data_per_position[3]= ['goals_scored', 'assists', 'bonus', 'total_points', 'was_home', 'minutes', 'yellow_cards', 'clean_sheets']
data_per_position[2] = ['goals_scored', 'assists', 'bonus', 'total_points', 'was_home', 'minutes', 'yellow_cards', 'clean_sheets']
data_per_position[1] = ['bonus', 'total_points', 'was_home', 'minutes', 'yellow_cards', 'saves', 'clean_sheets']
learner(2)
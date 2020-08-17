from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeRegressor
import matplotlib.pyplot as plt


def learner(position):

    x_df = pd.read_csv(data_path + 'cumulative_gw_2.csv')
    y_df = pd.read_csv(data_path + 'total_points_gw_2.csv')
    x_df = x_df.loc[x_df['position'] == position]  # select position
    y_df = y_df.loc[y_df['position'] == position]  # select position

    necessary_data = data_per_position[position]
    x_df = x_df[necessary_data]
    y_df = y_df['total_points']
    # x_df['was_home'] = x_df['was_home'].apply(lambda x: 1 if x == True else 0)
    # for parameter in necessary_data:
    #     x_df[parameter] = (x_df[parameter] - x_df[parameter].min())/x_df[parameter].max()

    x = x_df.to_numpy()
    y = y_df.to_numpy().reshape(-1)

    x = x.astype(float)
    y = y.astype(float)

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

    if position > 1:
        regressor = MLPRegressor(hidden_layer_sizes=(100, 100), solver='adam' , activation='logistic', max_iter=100000,
                                 learning_rate_init=0.0001, learning_rate='invscaling').fit(x_train, y_train)
    else:
        regressor = DecisionTreeRegressor(criterion='mse', splitter='best', max_depth=10, min_samples_split=0.2,
                                          min_samples_leaf=1, min_weight_fraction_leaf=0.0,
                                          max_features='auto').fit(x_train, y_train)
        # regressor = MLPRegressor(hidden_layer_sizes=(10, 10, 10), solver='adam', activation='logistic', max_iter=100000,
        #                          learning_rate_init=0.0001, learning_rate='invscaling').fit(x_train, y_train)
    output = regressor.predict(x_test)

    difference = abs(output - y_test)
    print('VARIANCE = ' + str(np.var(difference)))
    mse = difference.mean()
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
    result = 'perfect:', str(perfect/total),'good:', str(good/total), 'normal:', str(normal/total), 'bad:', str(bad/total)
    print(result)


def pie_chart(real, predicted):
    pass


data_path = 'mh_learning_data\\'
data_per_position = dict()
data_per_position[4] = ['goals_scored', 'assists', 'bonus', 'form', 'total_points', 'was_home', 'minutes', 'yellow_cards', 'red_cards', 'difficulty']
data_per_position[3]= ['goals_scored', 'assists', 'bonus', 'form', 'bps', 'total_points', 'was_home', 'minutes', 'yellow_cards', 'red_cards', 'clean_sheets', 'difficulty']
data_per_position[2] = ['goals_scored', 'assists', 'bonus', 'form', 'total_points', 'was_home', 'minutes', 'yellow_cards', 'red_cards', 'goals_conceded', 'clean_sheets', 'difficulty']
data_per_position[1] = ['bonus', 'bps', 'form', 'total_points', 'saves', 'goals_conceded', 'was_home', 'clean_sheets', 'yellow_cards', 'red_cards' ,'penalties_saved', 'difficulty']

learner(2)
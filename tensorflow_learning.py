from turtle import pos

import tensorflow as tf
from tensorflow import keras
import numpy as np
import pandas as pd
from datetime import datetime
from sklearn.model_selection import train_test_split

coefficients = dict()
coefficients[4] = [[4.],[3.],[1.],[0.016],[-1.]] #goal,assist,bonus,minutes,yellow_cards
coefficients[3] = [[5.],[3.],[1.],[0.016],[-1.],[1.]] #goal,assist,bonus,minutes,yellow_cards,clean_sheets
coefficients[2] = [[4.],[1.],[6.],[3.],[0.016],[-.5],[-1.]] #clean_sheets,bonus,goals_assists,minutes,goals_conceded,yellow_cards
coefficients[1] = [[4.],[1.],[.33],[0.016],[-.5]] #clean_sheets,bonus,saves,minutes,goals_conceded

class LastLayer(keras.layers.Layer):
    def __init__(self, units=32):
        super(LastLayer, self).__init__()
        self.units = units

    def build(self, input_shape):
        # goals, assists, clean_sheet, bonus, minutes
        self.w = tf.Variable(initial_value=np.array(coefficients[post]), dtype=tf.float32, trainable=False)

    def call(self, inputs):
        result = tf.matmul(inputs, self.w)
        return result


seasons = ['2018', '2019']
post = 2
size = len(coefficients[post])
data_path = 'mh_learning_data\\'
x = pd.read_csv(data_path + seasons[0] + '\\x.csv')
y = pd.read_csv(data_path + seasons[0] + '\\y.csv')

data_per_position = dict()
data_per_position[4] = ['goals_scored', 'assists', 'opponent_conceded', 'bonus', 'bps', 'form', 'total_points',
                        'minutes', 'yellow_cards', 'red_cards', 'difficulty']
data_per_position[3] = ['opponent_conceded', 'goals_scored', 'assists', 'bonus', 'form', 'bps', 'total_points',
                        'was_home', 'minutes', 'yellow_cards', 'red_cards', 'clean_sheets', 'difficulty']
data_per_position[2] = ['GW', 'goals_scored', 'assists', 'bonus', 'form', 'total_points',
                        'minutes','clean_sheets', 'goals_conceded', 'opponent_goals', 'yellow_cards', 'difficulty']
data_per_position[1] = ['GW', 'opponent_goals', 'bonus', 'minutes', 'bps', 'form', 'total_points', 'saves',
                        'goals_conceded', 'was_home', 'clean_sheets', 'yellow_cards', 'red_cards', 'penalties_saved',
                        'difficulty']
x = x.loc[x['position'] == post][data_per_position[post]].values.astype(float)
y = y.loc[y['position'] == post]['total_points'].values.astype(float)

x = (x - np.mean(x)) / np.std(x)

x_test, x_train, y_test, y_train = train_test_split(x, y, test_size=0.2)

model = keras.Sequential([
    keras.layers.Input(shape=(len(data_per_position[post]),), name='input'),
    keras.layers.Dense(100, activation='sigmoid'),
    keras.layers.Dense(200, activation='sigmoid'),
    keras.layers.Dense(size, activation='sigmoid'),
    LastLayer(1)
])
timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
callbacks = [keras.callbacks.TensorBoard(log_dir='logs/scalars/{}'.format(timestamp))]
model.compile(optimizer=keras.optimizers.Adam(), loss=keras.losses.MSE)
model.fit(x_train, y_train, validation_data=(x_test, y_test), batch_size=32, epochs=100, verbose=3, callbacks=callbacks)

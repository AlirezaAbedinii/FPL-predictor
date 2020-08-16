from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
import pandas as pd
import matplotlib.pyplot as plt

data_path = 'mh_learning_data\\'

x_df = pd.read_csv(data_path + 'cumulative_gw_2.csv')
y_df = pd.read_csv(data_path + 'total_points_gw_2.csv')

x_df = x_df.loc[x_df['position'] == 1] #select position
y_df = y_df.loc[y_df['position'] == 1] #select position

del x_df['position']
del y_df['position']

x_df = x_df.transpose()
y_df = y_df.transpose()

x_df = x_df.iloc[2:]
y_df = y_df.iloc[3:]

x_df = x_df.transpose()
y_df = y_df.transpose()


x_df['was_home'] = x_df['was_home'].apply(lambda x: 1 if x==True else 0)

del x_df['minutes']
del x_df['yellow_cards']
#del x_df['was_home']

x = x_df.to_numpy()
y = y_df.to_numpy().reshape(-1)

x = x.astype(int)
y = y.astype(int)

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

regressor = MLPRegressor(hidden_layer_sizes=(5,10,5), activation='logistic', max_iter=100000, learning_rate_init=0.001).fit(x_train, y_train)

output = regressor.predict(x_test)

mse = ((output - y_test)**2).mean()
print('MSE = ' + str(mse))
df = pd.DataFrame({'Actual': y_test.flatten(), 'Predicted': output.flatten()})
plt.scatter(y_test, output,  color='gray', alpha=0.5)
plt.show()
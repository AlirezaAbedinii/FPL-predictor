from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
import pandas as pd
from pycm import *

x_df = pd.read_csv('cumulative_gw_2.csv').transpose()
y_df = pd.read_csv('total_points_gw_2.csv').transpose()

x_df = x_df.iloc[2:]
y_df = y_df.iloc[2:]

x_df = x_df.transpose()
y_df = y_df.transpose()

del x_df['minutes']

x = x_df.to_numpy()
y = y_df.to_numpy().reshape(-1)

x = x.astype(int)
y = y.astype(int)

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

classifier = MLPClassifier(hidden_layer_sizes=(5,10,5), activation='relu', max_iter=100000).fit(x_train, y_train)

output = classifier.predict(x_test)

cm = ConfusionMatrix(y_test.flatten(), output)
cm.print_matrix()

mse = ((output - y_test)**2).mean()
print('MSE = ' + str(mse))
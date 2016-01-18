import numpy as np
from sklearn import datasets, preprocessing
from sklearn.cross_validation import train_test_split
import matplotlib.pyplot as plt
from neupy import algorithms, layers, environment


np.random.seed(0)
plt.style.use('ggplot')

environment.sandbox()


def rmsle(expected, actual):
    n_samples = actual.shape[0]
    square_logarithm_difference = np.log((expected + 1) / (actual + 1)) ** 2
    return np.sqrt((1. / n_samples) * np.sum(square_logarithm_difference))


dataset = datasets.load_boston()
data, target = dataset.data, dataset.target

data_scaler = preprocessing.MinMaxScaler(feature_range=(-3, 3))
target_scaler = preprocessing.MinMaxScaler()

data = data_scaler.fit_transform(data)
target = target_scaler.fit_transform(target)

x_train, x_test, y_train, y_test = train_test_split(
    data, target, train_size=0.85
)

cgnet = algorithms.QuasiNewton(
    connection=[
        layers.Sigmoid(13),
        layers.Sigmoid(50),
        layers.Sigmoid(10),
        layers.Output(1),
    ],
    show_epoch='100 times',
    verbose=True,
)

cgnet.train(x_train, y_train, x_test, y_test, epochs=100)
y_predict = cgnet.predict(x_test)

y_test = target_scaler.inverse_transform(y_test)
y_predict = target_scaler.inverse_transform(y_predict).T.round(1)
error = rmsle(y_predict, y_test)
print("RMSLE = {}".format(error))

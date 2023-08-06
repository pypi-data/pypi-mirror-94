import numpy as np


def euclidean_distance(x1, x2):
    return np.sqrt(np.sum((x1 - x2) ** 2))


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def accuracy(true, predicted):
    return np.sum(true == predicted) / len(true)


def mse(y_true, y_predicted):
    return np.mean((y_true - y_predicted)**2)

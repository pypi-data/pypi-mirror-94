import numpy as np
from MLibrary.utils import sigmoid


class BaseRegression:

    def __init__(self, lr=0.001, n_iters=1000):
        self.lr = lr
        self.n_iters = n_iters
        self.weights = None
        self.bias = None

    def fit(self, X, y):
        # init parameters
        n_samples, n_features = X.shape
        self.weights = np.zeros(n_features)
        self.bias = 0

        for _ in range(self.n_iters):
            # approximate
            y_predicted = self._approximation(X, self.weights, self.bias)

            dw = (1/n_samples) * np.dot(X.T, (y_predicted - y))     # weights derivative
            db = (1/n_samples) * np.sum(y_predicted - y)            # bias derivative

            # gradient descent
            self.weights -= self.lr * dw
            self.bias -= self.lr * db

    def predict(self, X):
        return self._predict(X, self.weights, self.bias)

    def _approximation(self, X, weights, bias):
        raise NotImplementedError()

    def _predict(self, X, weights, bias):
        raise NotImplementedError()


class LinearRegression(BaseRegression):

    def _approximation(self, X, weights, bias):
        return np.dot(X, weights) + bias

    def _predict(self, X, weights, bias):
        return np.dot(X, weights) + bias    # linear model


class LogisticRegression(BaseRegression):

    def _approximation(self, X, weights, bias):
        linear_model = np.dot(X, weights) + bias
        return sigmoid(linear_model)

    def _predict(self, X, weights, bias):
        linear_model = np.dot(X, weights) + bias    # linear_model + sigmoid
        y_predicted = sigmoid(linear_model)
        return [1 if i > 0.5 else 0 for i in y_predicted]

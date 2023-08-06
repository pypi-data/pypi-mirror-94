import numpy as np
from collections import Counter
from MLibrary.utils import euclidean_distance


class KNN:

    def __init__(self, k=3):
        """ k = number of neighbours to consider """
        self.k = k

    def fit(self, X, y):
        self.X_train = X    # values
        self.y_train = y    # labels

    def predict(self, X):
        """ get predicted labels for each x in X """
        predicted_labels = [self._predict(x) for x in X]
        return np.array(predicted_labels)

    def _predict(self, x):
        # compute distances
        distances = [euclidean_distance(x, x_train) for x_train in self.X_train]
        # get K nearest samples and labels
        k_indices = np.argsort(distances)[:self.k]
        k_nearest_labels = [self.y_train[i] for i in k_indices]
        # most common class label
        most_common = Counter(k_nearest_labels).most_common(1)
        return most_common[0][0]

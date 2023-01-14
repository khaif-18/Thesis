import pandas as pd
from .exceptions import DistanceException
from .utils import distance_matrix, find_majority, validity
from sklearn.metrics import accuracy_score

class MKNN(object):
    def __init__(self, n_neighbors=3, distance='euclidean'):
        self.distance_list = [
            'euclidean',
            'manhattan',
        ]

        self.n_neighbors = n_neighbors

        if distance not in self.distance_list:
            raise DistanceException('jarak {} tidak dikenal'.format(distance))
        
        self.distance_index = self.distance_list.index(distance)
        
        self.distance_method = self.distance_list[self.distance_index]

    def fit(self, X, y):
        self.X_train = X
        if isinstance(y, pd.Series):
            self.y = y.values.ravel()
        else:
            self.y = y

        self.distance = distance_matrix(X, X, self.distance_method)
        self.validity = validity(self.distance, self.y, self.n_neighbors)


    def predict(self, X_test):
        if isinstance(X_test, pd.Series):
            X_test = X_test.values
        else:
            X_test = X_test
            
        predicted_label = []
        distances = distance_matrix(X_test, self.X_train, self.distance_method)
        print(distances)
        for i in distances:
            weight = []
            for j in range(len(self.validity)):
                weight_j = self.validity[j] * (1 / (i[j] + 0.5))
                weight.append(weight_j)
            
            sorted_index = sorted(range(len(weight)), key=lambda n_neighbors: weight[n_neighbors], reverse = True)
            f_label = []
            y = self.y
            for i in range(self.n_neighbors):
                f_label.append(y[sorted_index[i]])
            
            majority, count = find_majority(f_label)
            print(f_label)
            predicted_label.append(majority)

        return predicted_label
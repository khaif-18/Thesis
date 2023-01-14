import pandas as pd
from .exceptions import DistanceException
from .utils import distance_matrix, find_majority
from sklearn.metrics import accuracy_score

class KNN(object):
    def __init__(self, n_neighbors=3, distance='euclidean'):
        self.distance_list = [
            'euclidean',
            'manhattan',
        ]

        self.n_neighbors =  n_neighbors

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


    def predict(self, X_test):
        if isinstance(X_test, pd.Series):
            X_test = X_test.values
        else:
            X_test = X_test
            
        predicted_label = []
        distances = distance_matrix(X_test, self.X_train, self.distance_method)
        
        current_index = 0
        for i in distances:
            sorted_index = sorted(range(len(i)), key=lambda n_neighbors: i[n_neighbors])
            f_label = []
            y = self.y
            for j in range(self.n_neighbors):
                f_label.append(y[sorted_index[j + 1]]) # tidak termasuk dirinya sendiri
            
            print('{} -> {}'.format(y[current_index], f_label)) #Cuma untuk print
            majority, count = find_majority(f_label)
            predicted_label.append(majority)
            current_index += 1

        return predicted_label
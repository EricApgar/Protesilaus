import pandas as pandas
from sklearn.model_selection import StratifiedKFold, cross_val_predict
# from sklearn.svm import SVC  # Holding for now because slow train time - see if another way.
from sklearn.tree import DecisionTreeClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
import time as time
import random as random

class DataMaster(object):

    input_data = pandas.DataFrame()  # Make Empty DataFrame
    truth_class = ""
    feature_classes = ""    
    truth_data = []
    feature_data = []

    def __init__(self):

        return

    def add_update_data(self, data_frame):

        self.input_data = data_frame  # Set property to loaded data frame.
        # Other option would be to send this function a path and then have this load the data, 
        # but Tyler said that was bad and this should be passed a data frame. 
        # Still not sure I agree...
        
    def set_truth_data(self):

        if not self.truth_class:  # String is empty, or no feature has been selected.
            print("Cant set truth data. No truth class feature selected.")  # Should never happen.
        else:
            self.truth_data = self.input_data[self.truth_class].values  # Get all data for truth set.
            self.feature_data = self.input_data.loc[:, (self.input_data.columns != self.truth_class)].values

    def train_all_models(self):

        preds = {"discr":self.train_discr(),
                 "cart":self.train_cart(),
                 "knn":self.train_knn(),
                 "nn":self.train_nn()}
        
        model_accuracy = 100 * sum(preds["discr"] == self.truth_data) / len(self.truth_data)
        print("{0:.2f}".format(model_accuracy))
        model_accuracy = 100 * sum(preds["cart"] == self.truth_data) / len(self.truth_data)
        print("{0:.2f}".format(model_accuracy))
        model_accuracy = 100 * sum(preds["knn"] == self.truth_data) / len(self.truth_data)
        print("{0:.2f}".format(model_accuracy))
        model_accuracy = 100 * sum(preds["nn"] == self.truth_data) / len(self.truth_data)
        print("{0:.2f}".format(model_accuracy))

    def train_discr(self):

        X = self.feature_data
        Y = self.truth_data

        kfolds_seed = random.randint(1, 10)
        kfolds = StratifiedKFold(n_splits=10, random_state=kfolds_seed)  # Maybe make once for class?
        model = LinearDiscriminantAnalysis(n_components=None, 
                                           priors=None, 
                                           shrinkage=None, 
                                           solver="svd", 
                                           store_covariance=False, 
                                           tol=0.0001)
        Y_pred = cross_val_predict(model, X, Y, cv=kfolds)

        return Y_pred

    def train_cart(self):

        X = self.feature_data
        Y = self.truth_data

        kfolds_seed = random.randint(1, 10)
        kfolds = StratifiedKFold(n_splits=10, random_state=kfolds_seed)  # Maybe make once for class?
        model = DecisionTreeClassifier()
        Y_pred = cross_val_predict(model, X, Y, cv=kfolds)
        
        return Y_pred

    def train_knn(self):

        X = self.feature_data
        Y = self.truth_data

        kfolds_seed = random.randint(1, 10)
        kfolds = StratifiedKFold(n_splits=10, random_state=kfolds_seed)  # Maybe make once for class?
        model = KNeighborsClassifier(n_neighbors=5)  # Arbitrarily choosing 5.
        Y_pred = cross_val_predict(model, X, Y, cv=kfolds)
        
        return Y_pred

    def train_nn(self):

        X = self.feature_data
        Y = self.truth_data

        kfolds_seed = random.randint(1, 10)
        kfolds = StratifiedKFold(n_splits=10, random_state=kfolds_seed)  # Maybe make once for class?
        model = MLPClassifier(solver='lbfgs', 
                              alpha=1e-5, 
                              hidden_layer_sizes=(10, 6), 
                              random_state=1)
        Y_pred = cross_val_predict(model, X, Y, cv=kfolds)
        
        return Y_pred
import pandas as pandas
from sklearn.model_selection import StratifiedKFold, cross_val_predict
# from sklearn.svm import SVC  # Holding for now because slow train time - see if another way.
from sklearn.svm import SVC  ## Slow on big data.
from sklearn.tree import DecisionTreeClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
import time as time
import random as random
import numpy as numpy

class DataMaster(object):

    input_data = pandas.DataFrame()  # Make Empty DataFrame
    truth_class = ""
    feature_classes = ""    
    
    truth_data = []
    feature_data = []

    scores = {"svm":numpy.nan,
              "discr":numpy.nan,
              "cart":numpy.nan,
              "knn":numpy.nan,
              "nn":numpy.nan}

    kfolds_seed = random.randint(1, 10)
    kfolds = StratifiedKFold(n_splits=10, random_state=kfolds_seed)

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

    def train_models(self, model_list):

        # Creat dictionary of kfolded predictions for every model.
        # Calculate kfolded accuracy for each model and store in class property.
        preds = {}
        for model in model_list:
            if model == "svm":
                preds[model], train_time = self.train_svm()
                self.scores[model] = 100 * sum(preds[model] == self.truth_data) / len(self.truth_data)
            elif model == "discr":
                preds[model] = self.train_discr()
                self.scores[model] = 100 * sum(preds[model] == self.truth_data) / len(self.truth_data)
            elif model == "cart":
                preds[model] = self.train_cart()
                self.scores[model] = 100 * sum(preds[model] == self.truth_data) / len(self.truth_data)
            elif model == "knn":
                preds[model] = self.train_knn()
                self.scores[model] = 100 * sum(preds[model] == self.truth_data) / len(self.truth_data)
            elif model == "nn":
                preds[model] = self.train_nn()
                self.scores[model] = 100 * sum(preds[model] == self.truth_data) / len(self.truth_data)
            else:
                print("ERROR: Model \"" + model + "\" not found.")

        # for value in self.scores.values():  # Print all scores to screen. DEBUGGING.
        #     print("{0:.2f}".format(value))

    def train_svm(self):

        X = self.feature_data
        Y = self.truth_data
        
        start_time = time.time()

        model = SVC(kernel='linear')
        Y_pred = cross_val_predict(model, X, Y, cv=self.kfolds)

        train_time = time.time() - start_time

        return Y_pred, train_time

    def train_discr(self):

        X = self.feature_data
        Y = self.truth_data
        
        model = LinearDiscriminantAnalysis(n_components=None, 
                                           priors=None, 
                                           shrinkage=None, 
                                           solver="svd", 
                                           store_covariance=False, 
                                           tol=0.0001)
        Y_pred = cross_val_predict(model, X, Y, cv=self.kfolds)

        return Y_pred

    def train_cart(self):

        X = self.feature_data
        Y = self.truth_data

        model = DecisionTreeClassifier()
        Y_pred = cross_val_predict(model, X, Y, cv=self.kfolds)
        
        return Y_pred

    def train_knn(self):

        X = self.feature_data
        Y = self.truth_data

        model = KNeighborsClassifier(n_neighbors=5)  # Arbitrarily choosing 5.
        Y_pred = cross_val_predict(model, X, Y, cv=self.kfolds)
        
        return Y_pred

    def train_nn(self):

        X = self.feature_data
        Y = self.truth_data

        model = MLPClassifier(solver='lbfgs', 
                              alpha=1e-5, 
                              hidden_layer_sizes=(10, 6), 
                              random_state=1)
        Y_pred = cross_val_predict(model, X, Y, cv=self.kfolds)
        
        return Y_pred
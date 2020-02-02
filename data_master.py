import pandas as pandas
from sklearn.model_selection import StratifiedKFold, cross_val_predict
# from sklearn.svm import SVC  ## Slow on big data.
# from sklearn.tree import DecisionTreeClassifier
# from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
# from sklearn.neighbors import KNeighborsClassifier
# from sklearn.neural_network import MLPClassifier
import time as time
import random as random
import numpy as numpy
from anonymous import Anonymous
from model_training.svm import ModelSVM
from model_training.neural_net import ModelNeuralNet
from model_training.knn import ModelKNN
from model_training.discrm import ModelDiscrm
from model_training.cart import ModelCART


class DataMaster(object):

    input_data = pandas.DataFrame()  # Make Empty DataFrame
    truth_class = ""
    feature_classes = ""    
    
    truth_data = []
    feature_data = []

    scores = {"svm":numpy.nan,
              "discrm":numpy.nan,
              "cart":numpy.nan,
              "knn":numpy.nan,
              "nn":numpy.nan}

    model_traits = {}

    kfolds_seed = random.randint(1, 10)
    kfolds = StratifiedKFold(n_splits=10, random_state=kfolds_seed)

    data_for_predict = pandas.DataFrame()
    preds_to_save = pandas.DataFrame()

    trained_models = {}  # Models trained on all data.

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

        
        # model_nn = ModelNeuralNet(self.input_data, self.truth_class)
        # model_knn = ModelKNN(self.input_data, self.truth_class)
        # model_discrm = ModelDiscrm(self.input_data, self.truth_class)
        # model_cart = ModelCART(self.input_data, self.truth_class)

        # Creat dictionary of kfolded predictions for every model.
        # Calculate kfolded accuracy for each model and store in class property.
        preds = {}
        for model in model_list:
            if model == "svm":
                model_svm = ModelSVM(self.input_data, self.truth_class)
                train_time = model_svm.train_time
                preds[model] = model_svm.predictions
                self.scores[model] = model_svm.accuracy
                self.trained_models["svm"] = model_svm.full_model

                # preds[model], train_time = self.train_svm()
                # self.scores[model] = 100 * sum(preds[model] == self.truth_data) / len(self.truth_data)
            elif model == "discrm":
                model_discrm = ModelDiscrm(self.input_data, self.truth_class)
                train_time = model_discrm.train_time
                preds[model] = model_discrm.predictions
                self.scores[model] = model_discrm.accuracy
                self.trained_models["discrm"] = model_svm.full_model

                # preds[model], train_time = self.train_discr()
                # self.scores[model] = 100 * sum(preds[model] == self.truth_data) / len(self.truth_data)
            elif model == "cart":
                model_cart = ModelCART(self.input_data, self.truth_class)
                train_time = model_cart.train_time
                preds[model] = model_cart.predictions
                self.scores[model] = model_cart.accuracy
                self.trained_models["cart"] = model_svm.full_model

                # preds[model], train_time = self.train_cart()
                # self.scores[model] = 100 * sum(preds[model] == self.truth_data) / len(self.truth_data)
            elif model == "knn":
                model_knn = ModelKNN(self.input_data, self.truth_class)
                train_time = model_knn.train_time
                preds[model] = model_knn.predictions
                self.scores[model] = model_knn.accuracy
                self.trained_models["knn"] = model_svm.full_model

                # preds[model], train_time = self.train_knn()
                # self.scores[model] = 100 * sum(preds[model] == self.truth_data) / len(self.truth_data)
            elif model == "nn":
                model_nn = ModelNeuralNet(self.input_data, self.truth_class)
                train_time = model_nn.train_time
                preds[model] = model_nn.predictions
                self.scores[model] = model_nn.accuracy
                self.trained_models["nn"] = model_svm.full_model

                # preds[model], train_time = self.train_nn()
                # self.scores[model] = 100 * sum(preds[model] == self.truth_data) / len(self.truth_data)
            else:  # Should never get here. Will break on statement after this print().
                print("ERROR: Model \"" + model + "\" not found.")
                # Need to actually error out here instead of just printing. TODO.

            self.model_traits[model] = Anonymous(predictions=preds[model], 
                                                 train_time=train_time, 
                                                 accuracy=self.scores[model])

        # for value in self.scores.values():  # Print all scores to screen. DEBUGGING.
        #     print("{0:.2f}".format(value))

    # def train_svm(self):

    #     X = self.feature_data
    #     Y = self.truth_data
        
    #     start_time = time.time()

    #     model = SVC(kernel='linear')
    #     Y_pred = cross_val_predict(model, X, Y, cv=self.kfolds)        

    #     self.trained_models["svm"] = model.fit(X, Y)

    #     train_time = time.time() - start_time

    #     return Y_pred, train_time

    # def train_discr(self):

    #     X = self.feature_data
    #     Y = self.truth_data
        
    #     start_time = time.time()

    #     model = LinearDiscriminantAnalysis(n_components=None, 
    #                                        priors=None, 
    #                                        shrinkage=None, 
    #                                        solver="svd", 
    #                                        store_covariance=False, 
    #                                        tol=0.0001)
    #     Y_pred = cross_val_predict(model, X, Y, cv=self.kfolds)

    #     self.trained_models["discr"] = model.fit(X, Y)

    #     train_time = time.time() - start_time

    #     return Y_pred, train_time

    # def train_cart(self):

    #     X = self.feature_data
    #     Y = self.truth_data

    #     start_time = time.time()

    #     model = DecisionTreeClassifier()
    #     Y_pred = cross_val_predict(model, X, Y, cv=self.kfolds)
        
    #     self.trained_models["cart"] = model.fit(X, Y)

    #     train_time = time.time() - start_time

    #     return Y_pred, train_time

    # def train_knn(self):

    #     X = self.feature_data
    #     Y = self.truth_data
        
    #     start_time = time.time()

    #     model = KNeighborsClassifier(n_neighbors=5)  # Arbitrarily choosing 5.
    #     Y_pred = cross_val_predict(model, X, Y, cv=self.kfolds)
        
    #     self.trained_models["knn"] = model.fit(X, Y)

    #     train_time = time.time() - start_time

    #     return Y_pred, train_time

    # def train_nn(self):

    #     X = self.feature_data
    #     Y = self.truth_data

    #     start_time = time.time()

    #     model = MLPClassifier(solver='lbfgs', 
    #                           alpha=1e-5, 
    #                           hidden_layer_sizes=(10, 6), 
    #                           random_state=1)
    #     Y_pred = cross_val_predict(model, X, Y, cv=self.kfolds)
        
    #     self.trained_models["nn"] = model.fit(X, Y)

    #     train_time = time.time() - start_time

    #     return Y_pred, train_time

    def predict_on_new_data(self, model, data):
        
        predictions = model.predict(data)

        return predictions

import pandas as pandas
from sklearn.model_selection import StratifiedKFold, cross_val_predict
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

    # kfolds_seed = random.randint(1, 10)
    # kfolds = StratifiedKFold(n_splits=10, random_state=kfolds_seed)

    data_for_predict = pandas.DataFrame()
    preds_to_save = pandas.DataFrame()

    trained_models = {}  # Models trained on all data.

    def __init__(self):

        return

    def check_for_mixed_data(self, data_frame):
        is_mixed_list = data_frame.applymap(type).nunique() > 1
        mixed_feat_list = [feat_name for feat_name in data_frame.columns if is_mixed_list[feat_name]]

        return mixed_feat_list

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
                model_svm = ModelSVM(self.input_data, self.truth_class)
                train_time = model_svm.train_time
                preds[model] = model_svm.predictions
                self.scores[model] = model_svm.accuracy
                self.trained_models["svm"] = model_svm.full_model
            elif model == "discrm":
                model_discrm = ModelDiscrm(self.input_data, self.truth_class)
                train_time = model_discrm.train_time
                preds[model] = model_discrm.predictions
                self.scores[model] = model_discrm.accuracy
                self.trained_models["discrm"] = model_discrm.full_model
            elif model == "cart":
                model_cart = ModelCART(self.input_data, self.truth_class)
                train_time = model_cart.train_time
                preds[model] = model_cart.predictions
                self.scores[model] = model_cart.accuracy
                self.trained_models["cart"] = model_cart.full_model
            elif model == "knn":
                model_knn = ModelKNN(self.input_data, self.truth_class)
                train_time = model_knn.train_time
                preds[model] = model_knn.predictions
                self.scores[model] = model_knn.accuracy
                self.trained_models["knn"] = model_knn.full_model
            elif model == "nn":
                model_nn = ModelNeuralNet(self.input_data, self.truth_class)
                train_time = model_nn.train_time
                preds[model] = model_nn.predictions
                self.scores[model] = model_nn.accuracy
                self.trained_models["nn"] = model_nn.full_model
            else:  # Should never get here. Will break on statement after this print().
                print("ERROR: Model \"" + model + "\" not found.")
                # Need to actually error out here instead of just printing. TODO.

            self.model_traits[model] = Anonymous(predictions=preds[model], 
                                                 train_time=train_time, 
                                                 accuracy=self.scores[model])

        # for value in self.scores.values():  # Print all scores to screen. DEBUGGING.
        #     print("{0:.2f}".format(value))

    def predict_on_new_data(self, model, data):
        
        predictions = model.predict(data)

        return predictions

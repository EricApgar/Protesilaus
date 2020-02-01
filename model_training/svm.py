import pandas as pandas
import random as random
from sklearn.model_selection import StratifiedKFold, KFold, cross_val_predict
from sklearn.svm import SVC, SVR  ## Slow on big data.
from anonymous import Anonymous
from model_type import calc_model_type
import time as time


class ModelSVM(object):  # Created from data frame and name of truth var.

    # Properties defined here are static, belong to the Class itself (not an instance) and will change all instances of the class.
    # They do not need the "self" reference.
    # See https://stackoverflow.com/questions/9056957/correct-way-to-define-class-variables-in-python for more details.

    def __init__(self, raw_data, truth_name):  # This is the constructor.
        # if data_frame is null:  # TODO: Better error checking for these input arguments.
        #     raise ValueError("Bad data_frame data")
        # elif truth_name is null:
        #     raise ValueError("asdfsa")

        self.raw_data = raw_data  # Data frame, slimmed to only relevant data from original loading.
        self.truth_name = truth_name  # String name of the truth feature.

        self.feat_data = pandas.DataFrame()  # Data frame for all feature data.
        self.feat_vals = []  # Values of the feature data.
        self.feat_vals_norm = []  # Values of the feature data, normalized.

        # Not sure advantage of anonymous object over dictionary at this point...
        self.k_folds = Anonymous(seed=random.randint(1, 10),  # Seed is random int between 1 and 10.
            num_kfolds=10,
            regression=[],
            classification=[])

        # k_folds = {"seed":random.randint(1, 10),  # Seed is random int between 1 and 10.
        #     "num_kfolds":10,
        #     "regression":[],
        #     "classification":[]}

        self.trained_models = {"regression":[],  # kfolds = StratifiedKFold(n_splits=10, random_state=kfolds_seed)
            "classification":[]}

        self.truth_data = pandas.DataFrame()  # Data frame for all truth data.
        self.truth_vals = []  # Values of the truth data.
        self.truth_vals_norm = []  # Values of the truth data, normalized.
        
        self.predictions = []  # Kfolded Predictions for estimating model accuracy.

        # Initialize some things.
        self.set_feat_data()
        self.set_truth_data()

        self.train_models()        

        return
        
    def set_kfolds(self):
        num_kfolds = self.k_folds.num_kfolds

        self.k_folds.regression = KFold(n_splits=num_kfolds)
        self.k_folds.classification = StratifiedKFold(n_splits=num_kfolds)

    def set_feat_data(self):
        self.feat_data = self.raw_data.loc[:, (self.raw_data.columns != self.truth_name)]
        self.feat_vals = self.feat_data.values
        self.feat_vals_norm = self.feat_data.values  # TODO: Need to normalize this.

    def set_truth_data(self):
        self.truth_data = self.raw_data[self.truth_name]  # Get all data for truth set.
        self.truth_vals = self.feat_data.values
        self.truth_vals_norm = self.truth_data.values  # TODO: Need to normalize this.

    def train_models(self):
        model_type = calc_model_type(self.raw_data, self.truth_name)  # Get regression or classification.

        if model_type == "regression":
            predictions, time = self.train_regression()
        elif model_type == "classification":
            predictions, time = self.train_classification()
        else:
            raise ValueError("Unknown model type.")

    def train_regression(self):
        x = self.feat_vals
        y = self.truth_vals

        start_time = time.time()

        model = SVR(kernel="rbf", C=100, gamma=0.1, epsilon=.1)
        predictions = cross_val_predict(model, x, y, cv=self.k_folds.regression)
        self.trained_models["regression"] = model.fit(x, y)

        train_time = time.time() - start_time

        return predictions, train_time

    def train_classification(self):
        x = self.feat_vals
        y = self.truth_vals

        start_time = time.time()

        model = SVC(kernel="linear")
        predictions = cross_val_predict(model, x, y, cv=self.k_folds.classification)
        self.trained_models["classification"] = model.fit(x, y)

        train_time = time.time() - start_time

        return predictions, train_time
import pandas as pandas
import random as random
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.svm import SVC  ## Slow on big data.
from anonymous import Anonymous


class ModelSVM(object):  # Created from data frame and name of truth var.

    # Properties defined here are static, belong to the Class itself (not an instance) and will change all instances of the class.
    # They do not need the "self" reference.
    # See https://stackoverflow.com/questions/9056957/correct-way-to-define-class-variables-in-python for more details.

    def __init__(self, data_frame, truth_name):  # This is the constructor.
        # if data_frame is null:  # TODO: Better error checking for these input arguments.
        #     raise ValueError("Bad data_frame data")
        # elif truth_name is null:
        #     raise ValueError("asdfsa")

        self.raw_data = pandas.DataFrame()  # Data frame, slimmed to only relevant data from original loading.
        self.truth_name = ""  # String name of the truth feature.

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

        return  # Do I need 

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
                preds[model], train_time = self.train_discr()
                self.scores[model] = 100 * sum(preds[model] == self.truth_data) / len(self.truth_data)
            elif model == "cart":
                preds[model], train_time = self.train_cart()
                self.scores[model] = 100 * sum(preds[model] == self.truth_data) / len(self.truth_data)
            elif model == "knn":
                preds[model], train_time = self.train_knn()
                self.scores[model] = 100 * sum(preds[model] == self.truth_data) / len(self.truth_data)
            elif model == "nn":
                preds[model], train_time = self.train_nn()
                self.scores[model] = 100 * sum(preds[model] == self.truth_data) / len(self.truth_data)
            else:  # Should never get here. Will break on statement after this print().
                print("ERROR: Model \"" + model + "\" not found.")
                # Need to actually error out here instead of just printing. TODO.

            self.model_traits[model] = Anonymous(predictions=preds[model], 
                                                 train_time=train_time, 
                                                 accuracy=self.scores[model])

        # for value in self.scores.values():  # Print all scores to screen. DEBUGGING.
        #     print("{0:.2f}".format(value))

    def train_svm(self):

        X = self.feature_data
        Y = self.truth_data
        
        start_time = time.time()

        model = SVC(kernel='linear')
        Y_pred = cross_val_predict(model, X, Y, cv=self.kfolds)        

        self.trained_models["svm"] = model.fit(X, Y)

        train_time = time.time() - start_time

        return Y_pred, train_time

    def predict_on_new_data(self, model, data):
        
        predictions = model.predict(data)

        return predictions

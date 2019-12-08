from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QLineEdit, QCheckBox, QFileDialog
from anonymous import Anonymous
import pandas as pandas
import numpy as np
from copy import deepcopy as deepcopy


class TabPredict(QWidget):

    name = "Predict"  # Still not sure about this property being here...
    model_traits = {}

    path_traits = {}  # Holds details for the prediction file path and save file path.

    data_for_pred = pandas.DataFrame()
    data_for_save = pandas.DataFrame()  # Same as data_for_pred but with predictions.

    def __init__(self, parent):

        super(TabPredict, self).__init__(parent)

        self.my_parent = parent  # Make parent TabGroup available to everything here.
        self.data_master = self.my_parent.parent().data_master  # Quick link to MainWindow's data_master.        

        label_left = 10
        label_top = 10
        label_width = 200
        label_height = 30

        prcnt_left = 200        
        prcnt_width = 40
        check_left = 275
        check_width = 30
        check_height = 30
        vert_offset = 40

        label = QLabel(self)
        label.setText("Model Type")
        label.setGeometry(label_left, label_top, label_width, label_height)

        label = QLabel(self)
        label.setText("Accuracy")
        label.setGeometry(prcnt_left, label_top, label_width, label_height)

        label = QLabel(self)
        label.setText("Predict?")
        label.setGeometry(check_left, label_top, label_width, label_height)

        # This list MUST match list of models in DataMaster.train_models().
        model_labels = {"svm":"Support Vector Machine:",
                        "discr":"Discriminant Classifier:",
                        "cart":"Random Forest:",
                        "knn":"K-Nearest-Neighbors:",
                        "nn":"Neural Network:"}

        label_top += vert_offset
        # Create the labels, check boxes for displaying performance numbers for all models.
        for model in model_labels:
            self.model_traits[model] = Anonymous(full_tag=model_labels[model],
                label_name=QLabel(self),
                label_score=QLineEdit(self),
                check_box=QCheckBox(self))

            self.model_traits[model].label_name.setText(self.model_traits[model].full_tag)
            self.model_traits[model].label_name.setGeometry(label_left, label_top, label_width, label_height)
            self.model_traits[model].label_score.setGeometry(prcnt_left, label_top, prcnt_width, label_height)
            self.model_traits[model].label_score.setReadOnly(True)
            self.model_traits[model].check_box.setGeometry(check_left, label_top, check_width, check_height)
            self.model_traits[model].check_box.setChecked(False)

            label_top += vert_offset

        label_top += 2*vert_offset

        self.path_traits["predict"] = Anonymous(label=QLabel(self),
            buton=QPushButton("Browse...", self),
            line_edit=QLineEdit(self),
            path="")
        self.path_traits["predict"].label.setText("Select a new data set to predict on using the trained models.")
        self.path_traits["predict"].label.setGeometry(label_left, label_top, 500, 20)  # setGeometry(left, top, width, height)
        label_top += vert_offset
        self.path_traits["predict"].buton.clicked.connect(self.on_btn_push_browse)
        self.path_traits["predict"].buton.setToolTip("Select new data set to make predictions on.")
        self.path_traits["predict"].buton.setGeometry(label_left, label_top, 90, 30)
        self.path_traits["predict"].line_edit.setGeometry(label_left+100, label_top, 500, 30)

        label_top += 2*vert_offset

        self.path_traits["save"] = Anonymous(label=QLabel(self),
            buton=QPushButton("Save", self),
            line_edit=QLineEdit(self),
            path="")
        self.path_traits["save"].label.setText("Select a new data set to predict on using the trained models.")
        self.path_traits["save"].label.setGeometry(label_left, label_top, 500, 20)  # setGeometry(left, top, width, height)
        label_top += vert_offset
        self.path_traits["save"].buton.clicked.connect(self.on_btn_push_save)
        self.path_traits["save"].buton.setToolTip("Select new data set to make predictions on.")
        self.path_traits["save"].buton.setGeometry(label_left, label_top, 90, 30)
        self.path_traits["save"].line_edit.setGeometry(label_left+100, label_top, 500, 30)

    def on_btn_push_browse(self):

        file_name = QFileDialog.getOpenFileName(self, "Select input data: ", "C:\'", "*.xlsx")  # TODO: start location
        file_name = file_name[0]  # Parse down to single arg of full file path.

        if not file_name:
            print("Bad input file.")
        else:
            data = pandas.read_excel(file_name)  # Read in data from excel to DataFrame.

            # Check that all the features you used to make the models are actually in this data set.
            input_feats = self.data_master.input_data.columns  # From original data, 
            feat_names = input_feats[input_feats != self.data_master.truth_class]
            if np.all(np.isin(feat_names, data.columns)):
                self.data_for_pred = data[feat_names.values]  # Data that you will now make predictions on.                

                self.path_traits["predict"].line_edit.setText(file_name)  # Set path to prediction data in display.
            else:
                print("Missing features needed for predictions.")

    def on_btn_push_save(self):

        file_name = QFileDialog.getSaveFileName(self, "Select save file: ", "C:\'", "*.xlsx")  # TODO: start location
        file_name = file_name[0]  # Parse down to single arg of full file path.

        if not file_name:
            print("Bad save file.")
        else:  # Good save file name.
            self.add_preds_to_save_data()

            self.data_for_save.to_excel(file_name)
            self.path_traits["save"].line_edit.setText(file_name)

    def add_preds_to_save_data(self):

        self.data_for_save = deepcopy(self.data_for_pred)

        # Loop through models, make predictions if check box checked.
        for model_name in self.model_traits:
            if self.model_traits[model_name].check_box.isChecked():
                model = self.data_master.trained_models[model_name]
                predictions = self.data_master.predict_on_new_data(model, self.data_for_pred)
                col_name = "Predicted " + self.data_master.truth_class + " - " + model_name
                self.data_for_save.insert(0, col_name, predictions)
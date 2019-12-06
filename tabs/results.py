from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QLineEdit, QCheckBox, QFileDialog
from data_master import DataMaster
from anonymous import Anonymous
import pandas as pandas
import numpy as np
from copy import deepcopy as deepcopy

class TabResults(QWidget):

    name = "Results"  # Still not sure about this property being here...
    model_traits = {}

    def __init__(self, parent):

        super(TabResults, self).__init__(parent)

        self.my_parent = parent  # Make parent TabGroup available to everything here.
        self.data_master = self.my_parent.parent().data_master  # Quick link to MainWindow's data_master.

        label_left = 10
        label_top = 10
        label_width = 200
        label_height = 30

        prcnt_left = 200        
        prcnt_width = 40
        time_left = 275
        time_width = 40
        check_left = 350
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
        label.setText("Train Time")
        label.setGeometry(time_left, label_top, label_width, label_height)

        label = QLabel(self)
        label.setText("Save?")
        label.setGeometry(check_left, label_top, label_width, label_height)

        label_top += vert_offset

        model_labels = {"svm":"Support Vector Machine:",
                        "discr":"Discriminant Classifier:",
                        "cart":"Random Forest:",
                        "knn":"K-Nearest-Neighbors:",
                        "nn":"Neural Network:"}

        # Create the labels, check boxes for displaying performance numbers for all models.
        for model in model_labels:
            self.model_traits[model] = Anonymous(full_tag=model_labels[model],
                label_name=QLabel(self),
                label_score=QLineEdit(self),
                train_time=QLineEdit(self),
                check_box=QCheckBox(self))
            
            self.model_traits[model].label_name.setText(self.model_traits[model].full_tag)
            self.model_traits[model].label_name.setGeometry(label_left, label_top, label_width, label_height)
            self.model_traits[model].label_score.setGeometry(prcnt_left, label_top, prcnt_width, label_height)
            self.model_traits[model].train_time.setGeometry(time_left, label_top, time_width, label_height)
            self.model_traits[model].check_box.setGeometry(check_left, label_top, check_width, check_height)
            self.model_traits[model].check_box.setChecked(True)

            label_top += vert_offset

        # Setup Browse button.
        btn_browse = QPushButton("Browse...", self)
        btn_browse.setToolTip("Browse to input data file.")
        btn_browse.setGeometry(label_left, label_top+100, 80, 30)
        btn_browse.clicked.connect(self.on_btn_push_browse)
        
        self.path_disp_pred = QLineEdit(self)  # Setup File path display.
        self.path_disp_pred.setGeometry(label_left+100, label_top+100, 500, label_height)

    def on_btn_push_browse(self):

        file_name = QFileDialog.getOpenFileName(self, "Select input data: ", "C:\'", "*.xlsx")  # TODO: start location
        file_name = file_name[0]  # Parse down to single arg of full file path.

        if not file_name:
            print("Bad input file.")
        else:
            data = pandas.read_excel(file_name)  # Read in data from excel to DataFrame.

            # Check that all the features you used to make the models are actually in this data set.
            feat_names = data.columns[data.columns != self.data_master.truth_class]
            if np.all(np.isin(feat_names, data.columns)):
                data_for_pred = data[feat_names.values]  # Data that you will now make predictions on.
                data_for_save = deepcopy(data_for_pred)

                # Loop through models, make predictions if check box checked.
                for model in self.model_traits:
                    if self.model_traits[model].check_box.isChecked():
                        predictions = self.data_master.predict_on_new_data(model, data)
                        col_name = "Predicted " + self.data_master.truth_class + "- " + model
                        data_for_save.insert(0, col_name, predictions)

            else:
                print("Missing features needed for predictions.")

    def add_update_results(self):

        for model in self.data_master.model_traits:
            accuracy = self.data_master.model_traits[model].accuracy
            train_time = self.data_master.model_traits[model].train_time
            self.model_traits[model].train_time.setText("{0:.2f}".format(train_time))
            self.model_traits[model].label_score.setText("{0:.2f}".format(accuracy))
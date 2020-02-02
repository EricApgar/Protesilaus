from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QLineEdit, QCheckBox, QFileDialog
from data_master import DataMaster
from anonymous import Anonymous


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

        label_top += vert_offset

        # This list MUST match list of models in DataMaster.train_models().
        model_labels = {"svm":"Support Vector Machine:",
                        "discrm":"Discriminant Classifier:",
                        "cart":"Random Forest:",
                        "knn":"K-Nearest-Neighbors:",
                        "nn":"Neural Network:"}

        # Create the labels, check boxes for displaying performance numbers for all models.
        for model in model_labels:
            self.model_traits[model] = Anonymous(full_tag=model_labels[model],
                label_name=QLabel(self),
                label_score=QLineEdit(self),
                train_time=QLineEdit(self))
                # check_box=QCheckBox(self)

            self.model_traits[model].label_name.setText(self.model_traits[model].full_tag)
            self.model_traits[model].label_name.setGeometry(label_left, label_top, label_width, label_height)
            self.model_traits[model].label_score.setGeometry(prcnt_left, label_top, prcnt_width, label_height)
            self.model_traits[model].label_score.setReadOnly(True)
            self.model_traits[model].train_time.setGeometry(time_left, label_top, time_width, label_height)
            self.model_traits[model].train_time.setReadOnly(True)

            label_top += vert_offset

        # On clicking Results tab, enable Predict tab.

    def add_update_results(self):

        for model in self.data_master.model_traits:
            accuracy = self.data_master.model_traits[model].accuracy
            train_time = self.data_master.model_traits[model].train_time
            self.model_traits[model].train_time.setText("{0:.2f}".format(train_time))
            self.model_traits[model].label_score.setText("{0:.2f}".format(accuracy))
            self.my_parent.tab_dict["Predict"].model_traits[model].label_score.setText("{0:.2f}".format(accuracy))
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QLineEdit, QCheckBox
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



from PyQt5.QtWidgets import QWidget, QLabel, QPushButton
from tabs.results import TabResults

class TabTrain(QWidget):

    name = "Train"  # Still not sure about this property being here...

    def __init__(self, parent):

        super(TabTrain, self).__init__(parent)

        self.my_parent = parent  # Make parent TabGroup available to everything here.
        self.data_master = self.my_parent.parent().data_master  # Quick link to MainWindow's data_master.        

        label = QLabel(self)
        label.setText("Just click TRAIN for now.")
        label.setGeometry(10, 10, 150, 20)  # setGeometry(left, top, width, height)

        btn_analyze = QPushButton("TRAIN MODELS", self)
        btn_analyze.setToolTip("Train all models on selected data.")
        btn_analyze.setGeometry(10, 50, 90, 30)
        btn_analyze.clicked.connect(self.on_btn_push_train)

    def on_btn_push_train(self):

        model_list = ["svm", "discr", "cart", "knn", "nn"]

        self.data_master.set_truth_data()
        self.data_master.train_models(model_list)
        self.my_parent.tab_dict["Results"].add_update_results()

        # Training finished, unlock results tab.
        tab_index = self.my_parent.tab_group.indexOf(self.my_parent.tab_group.findChild(TabResults))  # Find index of Data tab.
        self.my_parent.tab_group.setTabEnabled(tab_index, True)  # Data loaded successfully, unlock next tab.

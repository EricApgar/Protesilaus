from PyQt5.QtWidgets import QWidget, QLabel, QListWidget
from tabs.train import TabTrain
from pandas.api.types import is_string_dtype, is_numeric_dtype
from matplotlib.backends.backend_qt5agg import FigureCanvas


class TabData(QWidget):

    name = "Data"  # Still not sure about this property being here...

    def __init__(self, parent):

        super(TabData, self).__init__(parent)

        self.my_parent = parent  # Make parent TabGroup available to everything here.
        self.data_master = self.my_parent.parent().data_master  # Quick link to MainWindow's data_master.        

        label = QLabel(self)
        label.setText("Select a Feature for Prediction.")
        label.setGeometry(10, 10, 150, 20)  # setGeometry(left, top, width, height)

        self.feature_list = QListWidget(self)
        self.feature_list.setGeometry(10, 50, 100, 300)  # x, y, w, h
        self.feature_list.itemClicked.connect(self.feature_clicked)  # Link clicking feature to plotting it.

    def feature_clicked(self):

        selected_item = self.feature_list.selectedItems()
        self.data_master.truth_class = selected_item[0].text()  # Set truth class to selected feature.
        self.data_master.feature_classes = self.data_master.input_data.columns[self.data_master.input_data.columns != self.data_master.truth_class]
        
        # Disable check box for Discriminant Classifiers if Regression and not Classification.
        self.update_discrm_check_box()

        tab_index = self.my_parent.tab_group.indexOf(self.my_parent.tab_group.findChild(TabTrain))  # Find index of Data tab.
        self.my_parent.tab_group.setTabEnabled(tab_index, True)  # Feature selected, unlock next tab.
        
        self.visualize_feature()  # CURRENTLY WORKING ON THIS

    def update_feat_list(self, new_feat_list):

        self.feature_list.clear()
        self.feature_list.addItems(new_feat_list)

    def visualize_feature(self):

        feat_data_type = self.get_feat_data_type(self.data_master.input_data, self.data_master.truth_class)
        if feat_data_type == "string":
            # Good, plot histogram
            feat_data = self.data_master.input_data[self.data_master.truth_class]
            self.plot_feat_data_str(feat_data)
        else:
            a = 1

    def get_feat_data_type(self, data_frame, feat_name):
        
        if is_string_dtype(data_frame[feat_name]):
            return "string"
        elif is_numeric_dtype(data_frame[feat_name]):
            return "number"
        else:
            return "unknown"

    def plot_feat_data_str(self, feat_data):
        a = 1
        # Expecting a string array (so a list?)

    def update_discrm_check_box(self):
        feat_type = self.get_feat_data_type(self.data_master.input_data, self.data_master.truth_class)

        if feat_type == "string":  # Classification.
            self.my_parent.tab_dict["Predict"].model_traits["discrm"].check_box.setChecked(False)
            self.my_parent.tab_dict["Predict"].model_traits["discrm"].check_box.setEnabled(True)
        elif feat_type == "number":  # Regression.
            self.my_parent.tab_dict["Predict"].model_traits["discrm"].check_box.setChecked(False)
            self.my_parent.tab_dict["Predict"].model_traits["discrm"].check_box.setEnabled(False)
        else:
            raise ValueError("You selected a mixed truth feature.")
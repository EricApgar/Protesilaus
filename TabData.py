from PyQt5.QtWidgets import QWidget, QLabel, QListWidget
from TabTrain import TabTrain

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

        # if not self.data_input.empty:  # This should never happen?
        
        a = 1  # Avoiding dumb EOF error.

    def feature_clicked(self):

        selected_item = self.feature_list.selectedItems()
        self.data_master.truth_class = selected_item[0].text()  # Set truth class to selected feature.
        self.data_master.feature_classes = self.data_master.input_data.columns[self.data_master.input_data.columns != self.data_master.truth_class]
        
        tab_index = self.my_parent.tab_group.indexOf(self.my_parent.tab_group.findChild(TabTrain))  # Find index of Data tab.
        self.my_parent.tab_group.setTabEnabled(tab_index, True)  # Feature selected, unlock next tab.
        # TODO. Plot something cool when you click feature.

    def update_feat_list(self, new_feat_list):

        self.feature_list.clear()
        self.feature_list.addItems(new_feat_list)
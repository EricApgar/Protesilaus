from PyQt5.QtWidgets import QWidget, QLabel, QListWidget


class TabData(QWidget):

    name = "Data"  # Still not sure about this property being here...
    # index = 1  # Index of tab in relation to others, from left.

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
        self.data_master.truth_class = selected_item[0].text()
        
        # TODO. Plot something cool when you click feature.

    def update_feat_list(self, new_feat_list):

        self.feature_list.clear()
        self.feature_list.addItems(new_feat_list)
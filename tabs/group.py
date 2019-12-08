from PyQt5.QtWidgets import QWidget, QTabWidget, QVBoxLayout
from tabs.input import TabInput
from tabs.data import TabData
from tabs.train import TabTrain
from tabs.results import TabResults
from tabs.predict import TabPredict


class TabGroup(QWidget):

    def __init__(self, parent):

        super(TabGroup, self).__init__(parent)

        # width, height = self.get_dims(parent.width(), parent.height())
        # print(str(width) + " , " + str(height))

        self.tab_dict = {
            "Input":TabInput(self),
            "Data":TabData(self),
            "Train":TabTrain(self),
            "Results":TabResults(self),
            "Predict":TabPredict(self)}

        # Add all tabs to the tab group.
        self.tab_group = QTabWidget()  # Create Tab Group from widget.
        for _, tab in self.tab_dict.items():  # Loop through tab_dict...
            self.tab_group.addTab(tab, tab.name)  # Add tab to group.
        
        self.tab_group.setTabEnabled(self.tab_group.indexOf(self.tab_group.findChild(TabInput)), True)  # Enable input tab.
        self.tab_group.setTabEnabled(self.tab_group.indexOf(self.tab_group.findChild(TabData)), False)  # Disable all other tabs to start.
        self.tab_group.setTabEnabled(self.tab_group.indexOf(self.tab_group.findChild(TabTrain)), False)  # Disable all other tabs to start.
        self.tab_group.setTabEnabled(self.tab_group.indexOf(self.tab_group.findChild(TabResults)), False)  # Disable all other tabs to start.
        self.tab_group.setTabEnabled(self.tab_group.indexOf(self.tab_group.findChild(TabPredict)), True)  # Disable all other tabs to start.

        self.tab_group.currentChanged.connect(self.tab_changed)  # How to enable "Predict" tab.

        # Define layout of this QWidget.
        self.layout = QVBoxLayout(self)  # V = Vertical aligned layout.
        self.layout.addWidget(self.tab_group)  # Add the tab group to this layout.
        self.setLayout(self.layout)  # Set layout of QWidget to the tab group.
        self.setFixedWidth(1000)  # Define width of tab group.
        self.setFixedHeight(600)  # Define height of tab group.


    def get_dims(self, width, height):  # TODO.

        return (width, height)

    def tab_changed(self, click_index):

        # Other tabs are unlocked when you click a button. Predict tab is unlocked if you click the 
        # "Results" tab and "Predict" is disabled. This means you just hit "train models" on the train
        # tab and you want to view the results. You must view before predicting.
        clicked_results_tab = click_index == self.tab_group.indexOf(self.tab_group.findChild(TabResults))
        predict_is_locked = not self.tab_dict["Predict"].isEnabled()  # Results tab is disabled.

        if clicked_results_tab and predict_is_locked:
            self.tab_group.setTabEnabled(self.tab_group.indexOf(self.tab_group.findChild(TabPredict)), True)  # Disable all other tabs to start.
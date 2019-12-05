from PyQt5.QtWidgets import QWidget, QTabWidget, QVBoxLayout
from tabs.input import TabInput
from tabs.data import TabData
from tabs.train import TabTrain
from tabs.results import TabResults


class TabGroup(QWidget):

    def __init__(self, parent):

        super(TabGroup, self).__init__(parent)

        # width, height = self.get_dims(parent.width(), parent.height())
        # print(str(width) + " , " + str(height))

        self.tab_dict = {
            "Input":TabInput(self),
            "Data":TabData(self),
            "Train":TabTrain(self),
            "Results":TabResults(self)}

        # Add all tabs to the tab group.
        self.tab_group = QTabWidget()  # Create Tab Group from widget.
        for _, tab in self.tab_dict.items():  # Loop through tab_dict...
            self.tab_group.addTab(tab, tab.name)  # Add tab to group.
        
        self.tab_group.setTabEnabled(self.tab_group.indexOf(self.tab_group.findChild(TabInput)), True)  # Enable input tab.
        self.tab_group.setTabEnabled(self.tab_group.indexOf(self.tab_group.findChild(TabData)), False)  # Disable all other tabs to start.
        self.tab_group.setTabEnabled(self.tab_group.indexOf(self.tab_group.findChild(TabTrain)), False)  # Disable all other tabs to start.
        self.tab_group.setTabEnabled(self.tab_group.indexOf(self.tab_group.findChild(TabResults)), False)  # Disable all other tabs to start.

        # Define layout of this QWidget.
        self.layout = QVBoxLayout(self)  # V = Vertical aligned layout.
        self.layout.addWidget(self.tab_group)  # Add the tab group to this layout.
        self.setLayout(self.layout)  # Set layout of QWidget to the tab group.
        self.setFixedWidth(1000)  # Define width of tab group.
        self.setFixedHeight(500)  # Define height of tab group.


    def get_dims(self, width, height):  # TODO.

        return (width, height)

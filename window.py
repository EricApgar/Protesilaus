from PyQt5.QtWidgets import QMainWindow
from data_master import DataMaster
from tabs.group import TabGroup


class MainWindow(QMainWindow):

    def __init__(self):

        super(MainWindow, self).__init__()

        self.setWindowTitle("Protesilaus")

        self.data_master = DataMaster()
        
        # self.win_height = 10  # Ping monitor size for these dimensions.
        # self.win_width = 10

        self.tabs = TabGroup(self)  # Create instance of tab group class.

from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QLineEdit, QFileDialog
from PyQt5.QtWidgets import QScrollArea, QTableWidget, QVBoxLayout, QTableWidgetItem  # Everything for excel table.
from PyQt5.QtCore import Qt
import pandas as pandas
import os.path as path
from tabs.data import TabData


class TabInput(QWidget):
    
    name = "Input"  # Label for tab.
    data_file_path = ""  # Part of display, so included in UI.

    def __init__(self, parent):
        
        super(TabInput, self).__init__(parent)

        self.my_parent = parent  # Make parent TabGroup available to everything here.
        self.data_master = self.my_parent.parent().data_master  # Quick link to MainWindow's data_master.

        # Setup label for Browse button.
        label = QLabel(self)
        label.setText("Select input data file.")
        label.setGeometry(10, 10, 100, 20)  # setGeometry(left, top, width, height)

        # Setup Browse button.
        btn_browse = QPushButton("Browse...", self)
        btn_browse.setToolTip("Browse to input data file.")
        btn_browse.setGeometry(10, 50, 80, 30)
        btn_browse.clicked.connect(self.on_btn_push_browse)

        # Setup File path display (path selected when Browse is hit).
        self.path_disp = QLineEdit(self)
        self.path_disp.setGeometry(100, 50, 500, 30)

        # Setup excel table view into input data.
        self.win = QWidget(self)
        self.win.setGeometry(10, 100, 600, 300)
        scroll = QScrollArea()
        layout = QVBoxLayout()
        self.data_table = QTableWidget()
        scroll.setWidget(self.data_table)
        layout.addWidget(self.data_table)
        self.win.setLayout(layout)

    def on_btn_push_browse(self):

        extn_filter = "(*.xlsx *.csv *.txt)"  # Filetypes I can currently read.
        extensions = (".xlsx", ".csv", ".txt")

        browsed_file_path = QFileDialog.getOpenFileName(self, "Select input data: ", "C:\'", extn_filter)  # TODO: start location
        browsed_file_path = browsed_file_path[0]  # Parse down to single arg of full file path.

        path_exists = path.exists(browsed_file_path)
        is_good_extn = browsed_file_path.lower().endswith(extensions)
        if path_exists and is_good_extn: # If file you browsed to exists and has okay extention...            
            self.load_input_data(browsed_file_path)  # Load data from file path.
            self.data_file_path = browsed_file_path  # Set property now that good filepath confirmed.

            self.display_data(self.data_master.input_data)  # TODO: Call to function to view snippet/all of data.            

            # Set list of features in Data Tab.
            self.my_parent.tab_dict["Data"].update_feat_list(self.data_master.input_data.columns)

            tab_index = self.my_parent.tab_group.indexOf(self.my_parent.tab_group.findChild(TabData))  # Find index of Data tab.
            self.my_parent.tab_group.setTabEnabled(tab_index, True)  # Data loaded successfully, unlock next tab.

        else:
            print("Bad File Path selected.")  # TODO: Pop-up window to say bad path.

    def load_input_data(self, file_path):

        self.path_disp.setText(file_path)

        _, file_extension = path.splitext(file_path)
        
        # Load file based on file extension.
        data_input_raw = pandas.DataFrame()  # Initialize to empty data frame.
        if file_extension == ".xlsx":
            data_input_raw = pandas.read_excel(file_path)
        elif file_extension == ".csv":
            data_input_raw = pandas.read_csv(file_path)
        elif file_extension == ".txt":
            # This is super sketch. Lots of stuff its guessing at currently.
            # For now, doing nothing.
            # TODO: determine file separator. Store as sep.
            # data_input_raw = pandas.read_csv(file_path, sep=" ", header=None)
            a = 1
        else:
            # Do nothing right now. TODO: pop-up dialogue box saying problem loading data.
            a = 1

        self.data_master.add_update_data(data_input_raw)  # Add data frame to MainWindow.DataMaster.
        

    def display_data(self, display_this):
        data_frame = self.data_master.input_data
        self.data_table.setColumnCount(len(data_frame.columns))
        self.data_table.setRowCount(len(data_frame.index))
        self.data_table.setHorizontalHeaderLabels(data_frame.columns)
        for i in range(len(data_frame.index)):
            for j in range(len(data_frame.columns)):
                # cell_item = self.data_table.item(i, j)  # TODO: Make cell not editable.
                # cell_item.setFlags(cell_item.flags() ^ Qt.ItemIsEditable)
                self.data_table.setItem(i, j, QTableWidgetItem(str(data_frame.iloc[i, j])))

        self.win.show()
import sys
from PyQt5.QtWidgets import QApplication
from MainWindow import MainWindow


def Main():

    app = QApplication(sys.argv)  # Start instance of application.

    main_window = MainWindow()  # Create Main window.
    main_window.showMaximized()  # Make the window maximized.

    sys.exit(app.exec_())  # Exit gracefully.


Main()

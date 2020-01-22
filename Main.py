import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from window import MainWindow


# These 2 commands have something to do with making things work at multiple resolutions.
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

def Main():

    app = QApplication(sys.argv)  # Start instance of application.

    main_window = MainWindow()  # Create Main window.
    main_window.showMaximized()  # Make the window maximized.

    sys.exit(app.exec_())  # Exit gracefully.


Main()

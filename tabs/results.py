from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QLineEdit, QCheckBox, QFileDialog
from data_master import DataMaster
from anonymous import Anonymous
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure as FigureClass
# from matplotlib.pyplot import bar as BarPlot
from seaborn import barplot as BarPlot


class TabResults(QWidget):

    name = "Results"  # Still not sure about this property being here...
    model_traits = {}

    def __init__(self, parent):

        super(TabResults, self).__init__(parent)

        self.my_parent = parent  # Make parent TabGroup available to everything here.
        self.data_master = self.my_parent.parent().data_master  # Quick link to MainWindow's data_master.

        label_left = 10
        label_top = 10
        label_width = 200
        label_height = 30

        prcnt_left = 200        
        prcnt_width = 40
        time_left = 275
        time_width = 40
        vert_offset = 40

        label = QLabel(self)
        label.setText("Model Type")
        label.setGeometry(label_left, label_top, label_width, label_height)

        label = QLabel(self)
        label.setText("Accuracy")
        label.setGeometry(prcnt_left, label_top, label_width, label_height)

        label = QLabel(self)
        label.setText("Train Time")
        label.setGeometry(time_left, label_top, label_width, label_height)

        label_top += vert_offset

        # This list MUST match list of models in DataMaster.train_models().
        model_labels = {"svm":"Support Vector Machine:",
                        "discrm":"Discriminant Classifier:",
                        "cart":"Random Forest:",
                        "knn":"K-Nearest-Neighbors:",
                        "nn":"Neural Network:"}

        # Create the labels, check boxes for displaying performance numbers for all models.
        for model in model_labels:
            self.model_traits[model] = Anonymous(full_tag=model_labels[model],
                label_name=QLabel(self),
                label_score=QLineEdit(self),
                train_time=QLineEdit(self))
                # check_box=QCheckBox(self)

            self.model_traits[model].label_name.setText(self.model_traits[model].full_tag)
            self.model_traits[model].label_name.setGeometry(label_left, label_top, label_width, label_height)
            self.model_traits[model].label_score.setGeometry(prcnt_left, label_top, prcnt_width, label_height)
            self.model_traits[model].label_score.setReadOnly(True)
            self.model_traits[model].train_time.setGeometry(time_left, label_top, time_width, label_height)
            self.model_traits[model].train_time.setReadOnly(True)

            label_top += vert_offset

        # Create plot area for feature importance plot.
        self.feature_fig = FigureClass()
        self.plot_canvas = FigureCanvas(self.feature_fig)
        self.plot_canvas.setGeometry(400, 50, 800, 500)  # setGeometry(left, top, width, height)
        self.plot_canvas.setParent(self)  # Set canvas to be on TabData (self).

        self.fig_axes = {"Figure1":self.feature_fig.add_subplot(111)}

        # On clicking Results tab, enable Predict tab.

    def add_update_results(self):

        for model in self.data_master.model_traits:
            accuracy = self.data_master.model_traits[model].accuracy
            train_time = self.data_master.model_traits[model].train_time
            self.model_traits[model].train_time.setText("{0:.2f}".format(train_time))
            self.model_traits[model].label_score.setText("{0:.2f}".format(accuracy))
            self.my_parent.tab_dict["Predict"].model_traits[model].label_score.setText("{0:.2f}".format(accuracy))

    def plot_feature_importance(self):

        feature_importances = self.data_master.trained_models["cart"].feature_importances_
        feature_names = self.data_master.input_data.columns[(self.data_master.input_data.columns != self.data_master.truth_class)].values

        for _, axes in self.fig_axes.items():
            axes.clear()  # Clear axes of previous plot.

        # Set random properties of figure common to both types:
        fig_title = "Feature Importance"
        y_label = "Y-Something"
        x_label = "X-Something"

        figure_1 = BarPlot(feature_names, feature_importances, ax=self.fig_axes["Figure1"])
        figure_1.set_title(fig_title)
        figure_1.set(xlabel=x_label, ylabel=y_label)

        # figure_1 = distplot(truth_data, ax=self.fig_axes["Figure1"])
        # figure_1.set_title(fig_title)
        # figure_1.set(xlabel=x_label, ylabel=y_label)

        self.plot_canvas.draw_idle()
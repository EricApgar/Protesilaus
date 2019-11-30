import pandas as pandas

class DataMaster(object):

    input_data = pandas.DataFrame()  # Make Empty DataFrame
    truth_class = ""

    def __init__(self):

        return

    def add_update_data(self, data_frame):

        self.input_data = data_frame
        

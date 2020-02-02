# Description here.

def calc_class_or_regr(data_frame, truth_name):
    
    # Assumes data already been scrubbed:
    # Data frame is homogenous data types per column.
    # Really this is just a check to see if truth column is strings or numbers.
    if data_frame.dtypes[truth_name] == "object":
        return "classification"
    else:  # Really bad hack for now - if not mixed or string, prolly numeric.
        return "regression"

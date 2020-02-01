# This lets you create an object with a bunch of name-value pairs.
# Example below. You pass it the property names and values and it will
# let you refer to those properties with "." notation.

# var = Anonymous(predictions=my_dict, 
#                 train_time=5, 
#                 accuracy=pandas.DataFrame())
# var.train_time = 5

class Anonymous(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
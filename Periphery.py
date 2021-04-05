class Counter:

    def __init__(self, num_single_value_label, num_boolean_label, num_curve_label, num_map_label):
        self.num_single_value_label = num_single_value_label
        self.num_boolean_label = num_boolean_label
        self.num_curve_label = num_curve_label
        self.num_map_label = num_map_label


    def single_add(self):
        self.num_single_value_label += 1

    def boolean_add(self):
        self.num_boolean_label += 1

    def curve_add(self):
        self.num_curve_label += 1

    def map_add(self):
        self.num_map_label += 1


class Options:
    def __init__(self, Precision, Prefix, Verbose, Encoding):
        self.Precision = Precision
        self.Prefix = Prefix
        self.num_curve_label = Verbose
        self.num_map_label = Encoding

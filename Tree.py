import Tree as tree

from InformationGain import get_measurements_threshold, select_best_measurement, calculate_split_value
from PrepareData import get_class_count

class Tree:"""class to set and create tree"""
    def __init__(self, root, left=None, right=None):""""method defines basic tree structure"""
        self.root = root
        self.left = left
        self.right = right

    def __str__(self):"""string method to name each root"""
        msg = "Root: %s" % self.root
        if self.left:
            msg += "\n Left: %s" % self.left
        if self.right:
            msg += "\n\t Right: %s" % self.right
        return msg


def build_tree(training, measurements, target):"""method to build tree"""

    target_column = training.loc[:, target]"""locate target column for training set"""
    target_val = target_column.iloc[0]"""selects first row of traget column in dataframe"""
    if all(value == target_val for value in target_column):""""creates end tree nodes"""
        return tree.Tree(target_val)

    if not measurements:""""if not known attribute get class count and return majority reoccuring class"""
        classes = get_class_count(training, target)
        highest_count = 0
        majority_class = ""
        for key in classes:
            if classes[key] > highest_count:
                highest_count = classes[key]
                majority_class = key
        return tree.Tree(majority_class)

    measurement_thresholds = dict()
    for measurement in measurements:"""call method to split indexes for an attributes """
        measurement_thresholds[measurement] = get_measurements_threshold(training, measurement, target)

    best_gains, best_gains_index = calculate_split_value(training, measurement_thresholds, measurements, target)"""returns best infomation gain to best gain"""

    if not best_gains_index:""""if not best gain index return tree"""
        target_column = training.loc[:, target]
        target_val = target_column.iloc[0]
        return tree.Tree(target_val)

    split_measurement = select_best_measurement(best_gains)"""selects attribute with most information gain to learn from"""
    if isinstance(split_measurement, list):
        split_measurement = split_measurement[0]
    split_index = best_gains_index[split_measurement]
    split_measurement_value = training[split_measurement][split_index]

    measurements.remove(split_measurement)"""gets rid of target measure from data"""

    split_l = training[training[split_measurement] < split_measurement_value]"""splits left and right if attribute split is less than or grater than index of split"""
    split_r = training[training[split_measurement] >= split_measurement_value]

    return tree.Tree({split_measurement: split_measurement_value}, build_tree(split_l, measurements, target),
                     build_tree(split_r, measurements, target))"""returns a tree root, left , right nodes"""
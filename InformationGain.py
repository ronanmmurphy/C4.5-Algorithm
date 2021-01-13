
from Entropy import entropy_calc


def get_information_gain(values, target, measurement_index, measurement): """Compute the information gain"""
	"""  
	Formula: Ent(S)-sum(|Sv|/|S| * Ent(Sv))
     - Sv = Subset of S where measurement A has value v
     - |S| = size of S
    """
    all_values = len(values)
    split_value = values[measurement][measurement_index]

    left_split = values[values[measurement] < split_value]"""splits left and right for index"""
    right_split = values[values[measurement] >= split_value]

    entropy = entropy_calc(values, target)"""calculate entropy for target"""
    info_gain = entropy - (len(left_split) / float(all_values)) * entropy_calc(left_split, target) - (
        len(right_split) / float(all_values)) * entropy_calc(right_split, target)"""calculate information gain"""

    return info_gain

def calculate_split_value(df, measurement_thresholds, measurements, target):
    """Return best splits for each measurement"""
    split_value = dict()
    split_value_index = dict()
    split_value_index = dict()
    for measurement in measurements:
        split_value[measurement] = 0.0
        for split in measurement_thresholds:
            for measurement_index in measurement_thresholds[split]:
                split_information = get_information_gain(df, target, measurement_index, measurement)""""gets information gain and test on all characteristics and compare with original"""
                if split_information > split_value[measurement]:
                    split_value[measurement] = split_information
                    split_value_index[measurement] = measurement_index
    return split_value, split_value_index"""return best information gain"""


def get_measurements_threshold(training_data, measurement, target): """Returns indexes to split on for a certain measurement"""
    """arrange measurements"""
    ordered = training_data.sort_values([measurement, target])
    target_col = ordered.loc[:, target]

    """make two arrays, one keeps values other keeps index of value in dataframe"""
    target_values = target_col.as_matrix()
    target_index = list(target_col.index.values)

    """Choose close values different only in target class to find best threshold"""
    measurement_indexes = []
    counter = 0

    for value in target_values:"""counter in array"""
        if counter + 1 < len(target_values):
            if value != target_values[counter + 1]:
				"""add split to the list"""		
                measurement_indexes.append(target_index[counter])
        counter += 1

    """if measurement_indexes is empty checker"""
    if not measurement_indexes:
        return target_values[0]
    return measurement_indexes


def select_best_measurement(best_info_gains): """Return measurement with best information gain"""
    highest_info_gain = 0.0
    split_measurement = ""
    for info_gain in best_info_gains:
        if best_info_gains[info_gain] > highest_info_gain:
            split_measurement = info_gain

    """Return only measurement in best_info_gains if no information gain is > 0"""
    if split_measurement == "":
        return best_info_gains.keys()
    return split_measurement


def predict_classes(test_data_example, decision_tree):"""Use a test data and pre calculated training decision tree to predict target for test"""
    root = decision_tree.root
    if isinstance(root, dict):
        for key in root:"""depending certain attributes effects the outcome of the tree predicting target class"""
            if test_data_example[key] < root[key]:
                if decision_tree.left is None:
                    if decision_tree.right is None:
                        return root
                    else:
                        return decision_tree.right
                return predict_classes(test_data_example, decision_tree.left)
            else:
                if decision_tree.right is None:
                    if decision_tree.left is None:
                        return root
                    else:
                        return decision_tree.left
                return predict_classes(test_data_example, decision_tree.right)""""returns predicted left and right nodes from input data"""
    else:
        return root


def avg_accuracy(all_acc_totals):
    """Return the avg accuracy of all the values in the dictionary"""
    avg = 0.0
    for result in all_acc_totals:
        avg += all_acc_totals[result]
    return float(avg) / float(len(all_acc_totals)) * 100.0"""get accuracy percentage"""

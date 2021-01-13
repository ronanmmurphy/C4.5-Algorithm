import math

from PrepareData import get_class_count


def entropy_calc(data, target):
    """Calculate the entropy for all of data
	This is the measure of how messy the data set is
    The entropy formula is the occurance of each target result divided by the total number of samples,
    multiplied by the log base 2 of that result, all multiplied by -1
    """
    results = get_class_count(data, target)
    log2 = lambda x: math.log(x) / math.log(2)

	"""formula calculation"""
    entropy = 0.0
    for result in results.keys():
        result_as_fraction = float(results[result]) / len(data)
        entropy -= result_as_fraction * log2(result_as_fraction)
    return entropy
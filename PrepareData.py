import numpy
"""this class is used to prepare the data set"""

def split_df(df, split_ratio):
    """Splits training and testing data from the dataframe"""
	
    """returns shuffled data"""
    data_after_shuffle = df.sample(frac=1)

	"""assign ratio for data split 2/3 for train 1/3 for test"""
    split_ratio = 0.666
	"""assign training data using shuffled from top of data from bottom 2 thirds"""
    training = data_after_shuffle[0:int(numpy.ceil(len(df)*split_ratio))]
	"""assign test data using shuffled from top of data from top 1 third"""
    testing = data_after_shuffle[int(numpy.ceil(len(df)*split_ratio))+1:len(df)]
	
    return training, testing


def get_class_count(df, target):
    """Counts frequency of each class in data and returns results in a dictionary"""
    results = dict()
    target_col = df.loc[:, target]""""gets location in dataframe of target column"""

    for target_result in target_col:"""counts to see total amount of target results possible"""
        if target_result not in results:
            results[target_result] = 0
        results[target_result] += 1

    return results

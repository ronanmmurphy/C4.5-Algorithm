import argparse

import pandas as pandas

from InformationGain import predict_classes, avg_accuracy
from PrepareData import split_df
from Tree import build_tree


def import_csv(file_name,  names=None):
    """This method imports the csv file and converts it to a panada dataframe"""
    return pandas.read_csv(file_name, header=None, names=names, keep_default_na=False)


def main():""""Main run class to test algorithm"""
    parser = argparse.ArgumentParser()""""Initalise the parser"""
    parser.add_argument(""""add parser argument for the folder the files were data stored"""
        "--file-path"
    )
    parser.add_argument(""""add parser argument for the file name of the file where data stored"""
        "--filename",
        '-f'
    )
    parser.add_argument(""""add parser argument for column titles in file"""
        "--attributes",
        default=["body-length", "wing-length", "body-width", "wing-width"]
    )
    parser.add_argument(""""add parser argument for kind of owl"""
        "--target",
        default="type"
    )
    parser.add_argument("""add parser argument for training and test split"""
        "--split-factor",
        "-sf",
        default=float(.66)
    )
    args = parser.parse_args()

    filename = args.file_path + args.filename""""filename defined as joint parse between path and name to give location of file"""
    attributes = args.attributes + [args.target]""""Attribute columns joining titles and target"""
    csvdata = import_csv(filename, attributes

    accuracy_results = dict()
    classifications = []
    print("C4.5 Algorithm")

    for i in range(0, 10):
        num_prediction_correct = 0.00"""variable for number of predictions correct"""
        training, testing = split_df(csvdata, args.split_factor)""""split training and test with ratio 0.66"""

        measurements = training.columns.values.tolist()
        measurements.remove(args.target)"""remove target column after training completed"""

        decision_tree = build_tree(training, measurements, args.target)"""build a decision tree calling Tree class"""
        print("Tree: ")
        print(decision_tree)

        num_measurements = len(testing)

        for index, row in testing.iterrows():"""for loop for testing data"""
            class_prediction = predict_classes(row, decision_tree)
            class_actual = row[args.target]
            classifications.append("Predicted Class: %s , Actual Class: %s" % (class_prediction, class_actual))"""comparing actual target class with predicted"""
            if class_prediction == class_actual:""""comparator for actual and predicted"""
                num_prediction_correct += 1.0
        classification_accuracy = float(num_prediction_correct) / float(num_measurements)"""accuracy of testing calculation"""
        accuracy_results[i] = classification_accuracy
    print("Accuracy of Results: ", accuracy_results)
    average_accuracy = avg_accuracy(accuracy_results)"""Print accuracy and average accuracy"""
    print("Average Accuracy: ",average_accuracy)

    print("Results CSV file.")"""create csv file to show results"""
    with open("c45_resluts.csv",'w') as f:
        for result in classifications:
            f.write(result + "\n")
        f.close()


if __name__ == '__main__':
    main()

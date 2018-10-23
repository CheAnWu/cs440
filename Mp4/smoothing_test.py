import argparse
import numpy as np
from matplotlib import pyplot as plt

import reader
import naive_bayes as nb


def compute_accuracies(predicted_labels, dev_set, dev_labels):
    yhats = predicted_labels
    accuracy = np.mean(yhats == dev_labels)

    return accuracy


def main(args):
    print("Running test")

    laplaceVals = np.linspace(.1, 1, 10)
    print(laplaceVals)

    accuracies = []
    for currLaplaceVal in laplaceVals:
        print("Laplaceval:", float(currLaplaceVal))
        train_set, train_labels, dev_set, dev_labels = reader.load_dataset(args.training_dir, args.development_dir,
                                                                           args.stemming)
        predicted_labels = nb.naiveBayes(train_set, train_labels, dev_set, float(currLaplaceVal), dev_labels)
        # accuracy = compute_accuracies(predicted_labels, dev_set, dev_labels)
        # print("Laplaceval:", float(currLaplaceVal), "Accuracy:", accuracy)
        # accuracies.append(accuracy)

    # plt.plot(laplaceVals, accuracies)
    # plt.ylabel('Accuracy')
    # plt.xlabel('LaPlace Smoothing Parameter')
    # plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='CS440 MP4 Naive Bayes')

    parser.add_argument('--training', dest='training_dir', type=str, default='mp4_data/training',
                        help='the directory of the training data')
    parser.add_argument('--development', dest='development_dir', type=str, default='mp4_data/development',
                        help='the directory of the development data')
    parser.add_argument('--stemming', default=False, action="store_true",
                        help='Use porter stemmer')
    parser.add_argument('--laplace', dest="laplace", type=float, default=1.0,
                        help='Laplace smoothing parameter - default 1.0')
    args = parser.parse_args()
    main(args)

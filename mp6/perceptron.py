# perceptron.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Justin Lizama (jlizama2@illinois.edu) on 10/27/2018

"""
This is the main entry point for MP6. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""
import numpy as np

def classify(train_set, train_labels, dev_set, learning_rate, max_iter):
    """
    train_set - A Numpy array of 32x32x3 images of shape [7500, 3072]. --> [7500, 3073]
                This can be thought of as a list of 7500 vectors that are each
                3072 dimensional.  We have 3072 dimensions because there are
                each image is 32x32 and we have 3 color channels.
                So 32*32*3 = 3072
    train_labels - List of labels corresponding with images in train_set
    example: Suppose I had two images [X1,X2] where X1 and X2 are 3072 dimensional vectors
             and X1 is a picture of a dog and X2 is a picture of an airplane.
             Then train_labels := [1,0] because X1 contains a picture of an animal
             and X2 contains no animals in the picture.

    dev_set - A Numpy array of 32x32x3 images of shape [2500, 3072].
              It is the same format as train_set
    """
    # return predicted labels of development set


    weights = np.random.rand(3073)
    print(weights)
    results = np.zeros(7500)

    ones = np.ones((7500, 1))
    new_train = np.hstack((train_set, ones))
    new_labels = np.zeros(len(train_labels))

    for i in range(len(new_labels)):
        if train_labels[i]:
            new_labels[i] = 1
        else:
            new_labels[i] = -1

    # learn_rate_decrease = learning_rate/max_iter

#Training
    for epoch in range(max_iter):
        for image_count, image in enumerate(new_train):
            score = np.dot(image, weights)
            results[image_count] = np.sign(score)

            if results[image_count] != new_labels[image_count]:
                weights += [x * new_labels[image_count] * learning_rate for x in image]

        # learning_rate -= learn_rate_decrease
    print(weights)

#Testing
    dev_results = np.zeros((2500, 1))
    dev_ones = np.ones((2500, 1))
    new_dev = np.hstack((dev_set, dev_ones))

    for image_count, image in enumerate(new_dev):
        score = np.dot(image, weights)

        if np.sign(score) > 0:
            classification = 1
        else:
            classification = 0

        dev_results[image_count] = classification

    return dev_results












def classifyEC(train_set, train_labels, dev_set,learning_rate,max_iter):
    # Write your code here if you would like to attempt the extra credit
    return []

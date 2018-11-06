# viterbi.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Renxuan Wang (renxuan2@illinois.edu) on 10/18/2018

"""
This is the main entry point for MP5. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""

'''
TODO: implement the baseline algorithm.
input:  training data (list of sentences, with tags on the words)
        test data (list of sentences, no tags on the words)
output: list of sentences, each sentence is a list of (word,tag) pairs. 
        E.g., [[(word1, tag1), (word2, tag2)], [(word3, tag3), (word4, tag4)]]
'''

import numpy as np
import math


def baseline(train, test):
    predicts = []
    word_to_tag_counts = {}
    tag_totals = {}

    for sentence in train:
        for pair in sentence:
            word, tag = pair
            if tag in tag_totals:
                tag_totals[tag] += 1
            else:
                tag_totals[tag] = 1

            if word not in word_to_tag_counts:
                word_to_tag_counts[word] = {}
            if tag in word_to_tag_counts[word]:
                word_to_tag_counts[word][tag] += 1
            else:
                word_to_tag_counts[word][tag] = 1

    max_tag = getHighestValue(tag_totals)

    for sentence in test:
        sentence_prediction = []
        for word in sentence:
            if word in word_to_tag_counts:
                tag_map = word_to_tag_counts[word]
                best_tag = getHighestValue(tag_map)
                sentence_prediction.append((word, best_tag))
            else:
                sentence_prediction.append((word, max_tag))
        predicts.append(sentence_prediction)

    return predicts


<<<<<<< Updated upstream
def getHighestValue(tag_map):
    best_tag = max(tag_map.keys(), key=(lambda key: tag_map[key]))
    return best_tag


=======
>>>>>>> Stashed changes
'''
TODO: implement the Viterbi algorithm.
input:  training data (list of sentences, with tags on the words)
        test data (list of sentences, no tags on the words)
output: list of sentences with tags on the words
        E.g., [[(word1, tag1), (word2, tag2)], [(word3, tag3), (word4, tag4)]]
'''


def viterbi(train, test):
    word_to_tag_counts = {}
    tag_totals = {}

    tag_index = {}
    index_count = 0

    emission_smooth_param = 0.8

    for sentence in train:
        for pair in sentence:
            word, tag = pair

            if tag in tag_totals:
                tag_totals[tag] += 1
            else:
                tag_totals[tag] = 1
                tag_index[tag] = index_count
                index_count += 1

            if word not in word_to_tag_counts:
                word_to_tag_counts[word] = {}
            if tag in word_to_tag_counts[word]:
                word_to_tag_counts[word][tag] += 1
            else:
                word_to_tag_counts[word][tag] = 1

    # tag count per word/ total tag count - emission probability
    for key in word_to_tag_counts.keys():
<<<<<<< Updated upstream
        for tag in word_to_tag_counts[key].keys():
            word_to_tag_counts[key][tag] = (emission_smooth_param + word_to_tag_counts[key][tag]) / (
                tag_totals[tag] + emission_smooth_param * len(tag_totals))
=======
        for tag in tag_totals.keys():
            if tag in word_to_tag_counts[key]:
                word_to_tag_counts[key][tag] = (emission_smooth_param + word_to_tag_counts[key][tag]) / (
                            tag_totals[tag] + emission_smooth_param * len(tag_totals))
>>>>>>> Stashed changes

    initial_tag_probabilities = np.zeros(index_count)
    transition_matrix = np.zeros(shape=(index_count, index_count))

    for sentence in train:
        first = True
        for i in range(len(sentence[:-1])):
            word, tag = sentence[i]

            curr_tag_idx = tag_index[tag]

            if first:
                initial_tag_probabilities[curr_tag_idx] += 1
                first = False

            else:
                next_tag = sentence[i + 1][1]
                transition_matrix[curr_tag_idx][tag_index[next_tag]] += 1

    # not needed
    init_smooth_param = 0.5

    # count tag starts sentence / total num sentences
    for i in range(len(initial_tag_probabilities)):
        initial_tag_probabilities[i] = (initial_tag_probabilities[i]) / (len(train) + len(initial_tag_probabilities))

    transition_smooth_param = 0.5

    # LaPlace smoothing: (1+transition occurances)/(tag occurences + num tags)
    for tag, count in tag_totals.items():
        prev_idx = tag_index[tag]
        for i in range(len(transition_matrix)):
<<<<<<< Updated upstream
            transition_matrix[curr_idx][i] = (transition_matrix[curr_idx][i] + transition_smooth_param) / (
                count + transition_smooth_param * len(tag_totals))
=======
            transition_matrix[prev_idx][i] = (transition_matrix[prev_idx][i] + transition_smooth_param) / (
                        count + transition_smooth_param * len(tag_totals))
>>>>>>> Stashed changes

    for tag in tag_index.keys():
        print(tag)
    print(initial_tag_probabilities)
    print(transition_matrix)

<<<<<<< Updated upstream
    for sentence in test:
        trellis = np.zeros(shape=(len(sentence), len(tag_index)))
        first = True
=======
    tag_names = []
    for tag in tag_index.keys():
        tag_names.append(tag)

    for sentence in test:
        print("NEW SENTENCE**************************")
        trellis = []
>>>>>>> Stashed changes

        for i in range(len(sentence)):
            temp = []
            curr_word = sentence[i]

            print(tag_names[i])

            if i == 0:  # first word in sentence
                if curr_word not in word_to_tag_counts:
                    for tag in tag_index.keys():
                        probability = emission_smooth_param / (
<<<<<<< Updated upstream
                            tag_totals[tag] + emission_smooth_param * len(tag_totals))
                        trellis[0][tag_index[tag]] = initial_tag_probabilities[tag_index[tag]] * probability
=======
                                    tag_totals[tag] + emission_smooth_param * len(tag_totals))
                        tuple = (initial_tag_probabilities[tag_index[tag]] * probability, 'START')
                        temp.append(tuple)
>>>>>>> Stashed changes

                else:
                    for tag in tag_index.keys():

                        if tag not in word_to_tag_counts[curr_word]:
                            probability = emission_smooth_param / (
<<<<<<< Updated upstream
                                tag_totals[tag] + emission_smooth_param * len(tag_totals))
                            trellis[0][tag_index[tag]] = initial_tag_probabilities[tag_index[tag]] * probability
                        else:
                            probability = word_to_tag_counts[curr_word][tag]
                            trellis[0][tag_index[tag]] = initial_tag_probabilities[tag_index[tag]] * probability
=======
                                        tag_totals[tag] + emission_smooth_param * len(tag_totals))
                            tuple = (initial_tag_probabilities[tag_index[tag]] * probability, 'START')
                            temp.append(tuple)
                        else:
                            probability = word_to_tag_counts[curr_word][tag]
                            tuple = (initial_tag_probabilities[tag_index[tag]] * probability, 'START')
                            temp.append(tuple)
            else:
                probability = 0
                for tag in tag_index.keys():
                    prev_idx = tag_index[tag]

                    for j in range(len(tag_index)):
                        probability = -99999
                        if curr_word not in word_to_tag_counts:
                            probability = emission_smooth_param / (
                                    tag_totals[tag] + emission_smooth_param * len(tag_totals))
                        else:
                            if tag not in word_to_tag_counts[curr_word]:
                                probability = emission_smooth_param / (
                                        tag_totals[tag] + emission_smooth_param * len(tag_totals))
                            else:
                                probability = word_to_tag_counts[curr_word][tag]

                        if trellis[i - 1][prev_idx] == 0:
                            print("yooo")

                        prev_prob = trellis[i - 1][prev_idx]

                        log2 = np.log(transition_matrix[prev_idx][j])
                        log3 = np.log(probability)
                        probability = prev_prob[0] + log2 + log3

                        tuple = (probability, tag_names[prev_idx])
                        if prev_idx == 0:
                            temp.append(tuple)
                        elif (temp[j][0] < probability):
                            temp[j] = tuple
            trellis.append(temp)

        print("Printing trellis")
        print(trellis)
>>>>>>> Stashed changes

    predicts = []
    return predicts

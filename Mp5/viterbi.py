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

    max_tag = max(tag_totals.keys(), key=(lambda key: tag_totals[key]))

    for sentence in test:
        sentence_prediction = []
        for word in sentence:
            if word in word_to_tag_counts:
                tag_map = word_to_tag_counts[word]
                best_tag = max(tag_map.keys(), key=(lambda key: tag_map[key]))
                sentence_prediction.append((word, best_tag))
            else:
                sentence_prediction.append((word, max_tag))
        predicts.append(sentence_prediction)

    return predicts

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
    for key, value in word_to_tag_counts.items():
        word_to_tag_counts[key][value] = word_to_tag_counts[key][value]/tag_totals[value]


    initial_tag_probabilities = np.zeros(len(index_count))
    transition_matrix = np.zeros(shape = (len(index_count), len(index_count)))


    for sentence in train:
        first = True
        for i in sentence[:-1]:
            word, tag = sentence[i]

            curr_tag_idx = tag_index[tag]

            if first:
                initial_tag_probabilities[curr_tag_idx] += 1
                first = False

            else:
                next_tag = sentence[i+1][1]
                transition_matrix[curr_tag_idx][tag_index[next_tag]] += 1



    #Do we log this here?
    #count tag starts sentence / total num sentences
    for i in initial_tag_probabilities:
        initial_tag_probabilities[i] = initial_tag_probabilities[i]/len(train)



    #LaPlace smoothing: (1+transition occurances)/(tag occurences + num tags)
    for tag, count in tag_totals.items():
        curr_idx = tag_index[tag]
        for i in range(len(transition_matrix)):
            transition_matrix[curr_idx][i] = (transition_matrix[curr_idx][i] + 1)/ (count + len(tag_totals))

    print(initial_tag_probabilities)
    print(transition_matrix)



















    predicts = []
    return predicts

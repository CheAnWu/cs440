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
    predicts = []
    return predicts

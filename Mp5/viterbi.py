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
    tag_counts = {}
    most_likely_tags = {}

    for sentence in train:
        for pair in sentence:
            word, tag = pair
            if tag in most_likely_tags:
                most_likely_tags[tag] += 1
            else:
                most_likely_tags[tag] = 1

            if word not in tag_counts:
                tag_counts[word] = {}
            if tag in tag_counts[word]:
                tag_counts[word][tag] += 1
            else:
                tag_counts[word][tag] = 1

    max_tag = max(most_likely_tags.keys(), key=(lambda key: most_likely_tags[key]))

    for sentence in test:
        sentence_prediction = []
        for word in sentence:
            if word in tag_counts:
                tag_map = tag_counts[word]
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

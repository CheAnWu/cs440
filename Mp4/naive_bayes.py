# naive_bayes.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Justin Lizama (jlizama2@illinois.edu) on 09/28/2018

"""
This is the main entry point for MP4. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""
import numpy as np
import nltk

def parseIntoWordList(train_set, train_labels, isSpam):
    wordList = []
    wordCount = []

    for i in range(len(train_labels)):
        if (train_labels[i] != isSpam):
            continue
        curr_email = train_set[i]
        for word in curr_email:
            if word in wordList:
                wordCount[wordList.index(word)] += 1
            else:
                wordList.append(word)
                wordCount.append(1)

    return wordList, wordCount


# creates list of words with corresponding number = ('cat'in spam emails / all words in spam emails)
def createProbabilitiesList(words, wordcount, smoothing_param):

    problist = []
    total_words = sum(wordcount)
    total_types = len(words)

    unknown_prob = smoothing_param/(total_words + smoothing_param*(total_types + 1))

    for i in range(total_types):
        problist.append((wordcount[i] + smoothing_param) / (total_words + smoothing_param*(total_types + 1) ))

    return words, problist, unknown_prob

def parseIntoBigramList(train_set, train_labels, isSpam):
    bigram_list = []
    bigram_count = []

    for i in range(len(train_labels)):
        if (train_labels[i] != isSpam):
            continue
        curr_email = train_set[i]
        for j in range(len(curr_email)):
            if(j % 2 == 1):
                continue
            bigram = curr_email[j] + " " + curr_email[j + 1]
            if bigram in bigram_list:
                bigram_count[bigram_list.index(bigram)] += 1
            else:
                bigram_list.append(bigram)
                bigram_count.append(1)

    return bigram_list, bigram_count


def naiveBayes(train_set, train_labels, dev_set, smoothing_parameter):
    print("starting")
    """
    train_set - List of list of words corresponding with each email
    example: suppose I had two emails 'i like pie' and 'i like cake' in my training set
    Then train_set := [['i','like','pie'], ['i','like','cake']]

    train_labels - List of labels corresponding with train_set
    example: Suppose I had two emails, first one was spam and second one was ham.
    Then train_labels := [0,1]

    dev_set - List of list of words corresponding with each email that we are testing on
              It follows the same format as train_set

    smoothing_parameter - The smoothing parameter you provided with --laplace (1.0 by default)
    """

    # TODO: Write your code here
    # return predicted labels of development set
    spam_words, spam_wordcount = parseIntoWordList(train_set, train_labels, 1)
    ham_words, ham_wordcount = parseIntoWordList(train_set, train_labels, 0)







    spamWords, spamProbs, spamUNK = createProbabilitiesList(spam_words, spam_wordcount, smoothing_parameter)
    hamWords, hamProbs, hamUNK = createProbabilitiesList(ham_words, ham_wordcount, smoothing_parameter)

    loggedSpam = np.log(spamProbs)
    loggedSpamUNK = np.log(spamUNK)
    loggedHam = np.log(hamProbs)
    loggedHamUNK = np.log(hamUNK)

    dev_labels = []

    for i in range(len(dev_set)):
        probSpam = 0
        probHam = 0

        for word in dev_set[i]:
            if word in spamWords:
                index = spamWords.index(word)
                probSpam += loggedSpam[index]
            else:
                probSpam += loggedSpamUNK

            if word in hamWords:
                index = hamWords.index(word)
                probHam += loggedHam[index]
            else:
                probHam += loggedHamUNK

        if(probSpam > probHam):
            dev_labels.append(1)
        else:
            dev_labels.append(0)

    return dev_labels
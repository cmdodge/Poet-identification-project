#!/usr/bin/python

import random
import collections
import math
import sys
from collections import Counter
from util import *
from feature import *
from itertools import izip

"""
Multi-Class Classifier for Poets

To run, list author names in authorNames global dict. Note: there must be an existing file <author-name>.txt 
in the working directory that contains all of the author's works.
"""

cmuDict = {}
cmuVowels = []
authorNames = ["philip-larkin", 
                "william-shakespeare", 
                "robert-frost", 
                "emily-dickinson", 
                "sylvia-plath", 
                "allen-ginsberg", 
                "percy-bysshe-shelley", 
                "robert-lowell", 
                "e-e-cummings", 
                "elizabeth-bishop"]

def fullFeatureExtractor(poem):
    
    featureVector = Counter()
    #featureVector = extractBigramFeatures(poem, featureVector)
    
    #featureVector = ShakespeareLarkinFrost(poem, featureVector)
    # featureVector = hasRhymingWords(poem, featureVector)
    # featureVector = hasRhymingLines(poem, featureVector, cmuDict)
    # featureVector = hasEnjambment(poem, featureVector)
    # featureVector = extractWordFeatures(poem, featureVector)
    # featureVector = averageWordLength(poem, featureVector)
    #featureVector = poemLength(poem, featureVector)
    # featureVector = hasSimile(poem, featureVector)
    # featureVector = hasAlliteration(poem, featureVector, cmuDict, cmuVowels)
    # featureVector = hasAssonance(poem, featureVector, cmuDict, cmuVowels)
    #featureVector = averageSentenceLength(poem, featureVector)
    # featureVector = rhymeScheme(poem, featureVector, examples)
    
    return featureVector    


def learnPredictor(trainExamples, testExamples, featureExtractor):
    weightVectors = [{} for i in xrange(len(authorNames))]

    # predictor function
    def predictor(x):
        phix = featureExtractor(x)
        scores = [dotProduct(weightVec, phix) for weightVec in weightVectors]
        best = max(scores)

        for i in xrange(len(scores)):
            if best == scores[i]:
                return authorNames[i]

    numIters = 20
    eta = 0.01 #step-size

    for t in range(numIters):
        trainExamples = random.sample(trainExamples, len(trainExamples))
        for x, y in trainExamples:
            phix = featureExtractor(x)
            scores = [dotProduct(weightVec, phix) for weightVec in weightVectors]

            correctScore = 0
            correctW = {}
            maxIncorrect = 0
            maxIncorrectW = {}

            correctIndex = 0
            maxIncorrectIndex = 0

            for i in xrange(len(authorNames)):
                author = authorNames[i]
                if y == author:
                    correctIndex = i
                    maxIncorrectIndex = 0
                    for j in xrange(len(scores)):
                        if j != i and scores[j] > scores[maxIncorrectIndex]:
                            maxIncorrectIndex = j
                    break

            correctScore = scores[correctIndex]
            correctW = weightVectors[correctIndex]
            maxIncorrectScore = scores[maxIncorrectIndex]
            maxIncorrectW = weightVectors[maxIncorrectIndex]

            margin = correctScore - maxIncorrect

            if (margin < 1):
                increment(weightVectors[correctIndex], eta, phix)
                increment(weightVectors[maxIncorrectIndex], -1*eta, phix)

        print "Training percentage: %f" % evaluatePredictor(trainExamples, predictor, False)
        print "Test percentage: %f" % evaluatePredictor(testExamples, predictor, False)


def main():
    cmuDict = readExamples('cmudict.0.7a.txt')
    cmuVowels = readSymbols('cmudict.0.7a.vowel_symbols .txt')

    random.seed(1) # TEMPORARY

    trainExamples = []
    testExamples = []

    for i in xrange(len(authorNames)):
        author = authorNames[i]
        works = readAuthorExamples(author, author)
        random.shuffle(works)
        splitPt = 3 * len(works) / 4
        trainExamples += works[:splitPt]
        testExamples += works[splitPt:]

    random.shuffle(trainExamples)
    random.shuffle(testExamples)
    learnPredictor(trainExamples, testExamples, fullFeatureExtractor)


if __name__ == '__main__':
    main()
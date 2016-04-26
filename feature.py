import collections
from collections import Counter
import string
import sys
from pprint import pprint
# from util import *

# helper function for metrical pattern and iambicPentameterLevel - produces string representing meter
def computeMeter(line):
	meter = ""
	for word in line.replace('-',' ').split(): # split hyphenated words
		conformedWord = word.upper().translate(None, string.punctuation) # convert to uppercase, no punctuation
		if conformedWord in examples:
			syllables = examples[conformedWord] # get cmu dictionary entry
			for syllable in syllables:
				lastChar = syllable[len(syllable)-1]
				if lastChar.isdigit():
					if lastChar == '0':
						meter += "0"
					else:
						meter += "1"
	return meter

# helper function for iambicPentameterLevel - produces iambic pentameter
def computeIambicPentameter(length):
	meter = ""
	for i in xrange(length):
		if i % 2 == 0:
			meter += "0"
		else:
			meter += "1"
	return meter

# extracts the meter as a string of 1's and 0's for stressed and unstressed syllables. Increments the count
# in the feature vector of each metrical pattern found
def metricalPattern(poem, featureVector):
	for line in poem:
		meter = computeMeter(line)
		featureVector["meter-" + meter] += 1
	#print poem[0]
	#print featureVector
	return featureVector

# uses dynamic programming to compute Levenshtein edit distance between 2 strings
def editDistance(meter1, meter2):
	#print meter1
	#print meter2
	M = [[0 for i in xrange(len(meter2)+1)] for j in xrange(len(meter1)+1)]
	#pprint(M)
	M[0][0] = 0
	for i in xrange(len(meter1)+1):
		M[i][0] = i
	for j in xrange(len(meter2)+1):
		M[0][j] = j

	for i in xrange(1, len(meter1)+1):
		for j in xrange(1, len(meter2)+1):
			if meter1[i-1] == meter2[j-1]:
				M[i][j] = M[i-1][j-1]
			else:
				M[i][j] = min([M[i-1][j-1]+1, M[i-1][j]+1, M[i][j-1]+1])
	return M[len(meter1)][len(meter2)]


# computes average edit distance of line's meter from iambic pentameter
def iambicPentameterLevel(poem, featureVector):
	totalDist = 0
	for line in poem:
		meter = computeMeter(line)
		iambicPentameter = computeIambicPentameter(len(meter))
		totalDist += editDistance(meter, iambicPentameter)
	totalDist = totalDist/float(len(poem)) 
	featureVector["iambicPentameter"] = 1 / (totalDist+0.001)
	return featureVector

def readExamples(path):
	examples = {}
	for line in open(path):
		entry = line.split()
		examples[entry[0]] = entry[1:]
	return examples

def readSymbols(path):
	symbols = []
	for line in open(path):
		symbols.append(line)
	return symbols

def rhymeScheme(poem, featureVector, examples):
	ends = []
	for line in poem:
		if line != "":
			x = line.split()
			ends.append(x[len(x)-1])
	scheme = [-1 for x in range(len(poem))]
	scheme[0] = 0
	for x in range(1, len(ends)):
		if rhymingWords(ends[0], ends[x], examples) > 0:
			scheme[x] = 0
	marker = 0
	for x in range(len(ends)):
		if scheme[x] < 0:
			marker += 1
			scheme[x] = marker
			for y in range(x, len(ends)):
				if rhymingWords(ends[x], ends[y], examples) > 0:
					scheme[y] = marker
	
	for x in range(len(scheme)-1):
		if scheme[x] == scheme[x+1]: 
			featureVector['hasRhymingCouplet'] += 1
		if x < len(scheme)-2 and scheme[x] == scheme[x+2]: 
			featureVector['hasAlternatingRhyme'] += 1
	return featureVector

def rhymingWords(s1, s2, examples):
	s1 = s1.translate(string.maketrans("",""), string.punctuation) 
	s2 = s2.translate(string.maketrans("",""), string.punctuation)
	if s1.upper() not in examples or s2.upper() not in examples: return 0
	# return number of rhyming phonemes
	phone1 = examples[s1.upper()]
	phone2 = examples[s2.upper()]
	syllables = 0
	for i in range(1, min(len(phone1), len(phone2))):
		
		if phone1[len(phone1)-i] != phone2[len(phone2)-i]:
				# print syllables
				return syllables
		else:
			if ('0' in phone1[len(phone1)-i]) or ('1' in phone1[len(phone1)-i]) or ('2' in phone1[len(phone1)-i])\
			 or ('0' in phone2[len(phone2)-i]) or ('1' in phone2[len(phone2)-i]) or ('2' in phone2[len(phone2)-i]):
				syllables += 1
			if i == min(len(phone1), len(phone2)) - 1:
				return syllables 
			
def hasRhymingWords(poem, featureVector):
	# x is a poem/line/verse
	for line in poem:
		x = line.split()
		for i in range(len(x)-1):
			if rhymingWords(x[i], x[i+1], examples) >= 1:
				featureVector['hasRhyme'] += 1
	return featureVector

def hasRhymingLines(poem, featureVector, examples):
	ends = []
	for line in poem:
		if line != "":
			x = line.split()
			ends.append(x[len(x)-1])
	checked = []
	for w1 in ends:
		for w2 in ends:
			if w1 != w2 and rhymingWords(w1, w2, examples) > 0 and w1 not in checked:
				featureVector['hasRhyme'] += 1
				checked.append(w1)
				checked.append(w2)
	return featureVector

def hasCaesura(poem, featureVector):
	punctuation = '.,:!?;'
	for line in poem:
		if line != "":
			for i in range(len(punctuation)):
				if punctuation[i] in line[0:len(line)-1]:
					#print punctuation[i], line
					featureVector['hasCaesura'] += 1
	return featureVector

def hasEnjambment(poem, featureVector):
	for line in poem:
		if line != "":
			if line[len(line)-1] not in '.,:!?;-':
				featureVector['hasEnjambment'] += 1
	return featureVector

def extractWordFeatures(poem, featureVector):
    """
    Extract word features for a string x.
    @param string x: 
    @return Counter: sparse feature vector representation of x.
    Example: "I am what I am" --> {'I': 2, 'am': 2, 'what': 1}
    """
    for line in poem:
    	for word in line.translate(None, string.punctuation).split():
        	featureVector[word] += 1
    return featureVector

def extractBigramFeatures(poem, featureVector):
	poemStr = " ".join(poem)
	words = poemStr.split()
	for i in xrange(len(words) - 1):
		#featureVector[words[i] + "-" + words[i+1].translate(None, string.punctuation)] += 1
		featureVector[words[i].translate(None, string.punctuation).upper() + "-" + words[i+1].translate(None, string.punctuation)] += 1
	return featureVector

def averageWordLength(poem, featureVector):
	numWords = 0
	for line in poem:
		for word in line.split():
			featureVector['avgWordLength'] += len(word)
		numWords += len(line.split())
	featureVector['avgWordLength'] = featureVector['avgWordLength']/(1.0 * numWords)
	return featureVector

def poemLength(poem, featureVector):
	# length is given by the number of lines
	featureVector['poemLength'] = len(poem)
	return featureVector

def hasSimile(poem, featureVector):
	for line in poem:
		for word in line.split():
			if word == 'like' or word == 'as':
				featureVector['hasSimile'] += 1
	return featureVector

def hasAlliteration(poem, featureVector, examples, vowels):
	for lineStr in poem:
		line = lineStr.split()
		for i in range(len(line) - 1):
			s1 = line[i]
			s2 = line[i+1]

			if s1.upper() not in examples or s2.upper() not in examples: break

			if (examples[s1.upper()])[0] == (examples[s2.upper()])[0] and \
				(examples[s1.upper()])[0] not in vowels:
				featureVector['hasAlliteration'] += 1
	return featureVector

def hasAssonance(poem, featureVector, examples, vowels):
	for lineStr in poem:
		line = lineStr.split()
		for i in range(len(line) - 1):
			s1 = line[i]
			s2 = line[i+1]

			if s1.upper() not in examples or s2.upper() not in examples: break
			phone1 = examples[s1.upper()]
			phone2 = examples[s2.upper()]
			for item in phone1:
				if item in phone2 and item in vowels:
					featureVector['hasAssonance'] += 1
	return featureVector


def averageSentenceLength(poem, featureVector):
	currentSentence = 0
	x = ''.join(poem)
	(x.replace('!', '.')).replace('?', '.')
	for sentence in x.split('.'):
		featureVector['averageSentenceLength'] += len(sentence)
	featureVector['averageSentenceLength'] /= 1.0 * len(x.split('.'))
	return featureVector


examples = readExamples('cmudict.0.7a.txt')
vowels = readSymbols('cmudict.0.7a.vowel_symbols .txt')

#meter1 = "010"
#meter2 = "1111"
#meter1 = "kitten"
#meter2 = "sitting"
#print editDistance(meter1, meter2)
"""
poem = ['Faith is a fine invention', 'For Gentlemen who see!', 'But Microscopes are prudent', 'In an Emergency!']

poem = [
'There is a singer everyone has heard,',
'Loud, a mid-summer and a mid-wood bird,',
'Who makes the solid tree trunks sound again.',
'He says that leaves are old and that for flowers',
'Mid-summer is to spring as one to ten.',
'He says the early petal-fall is past',
'When pear and cherry bloom went down in showers',
'On sunny days a moment overcast;',
'And comes that other fall we name the fall.',
'He says the highway dust is over all.',
'The bird would cease and be as other birds',
'But that he knows in singing not to sing.',
'The question that he frames in all but words',
'Is what to make of a diminished thing.']

featureVector = Counter()

featureVector = metricalPattern(poem)
print featureVector
"""
"""
featureVector = hasRhymingWords(poem, featureVector)

featureVector = hasRhymingLines(poem, featureVector, examples)

featureVector = hasEnjambment(poem, featureVector)

featureVector = extractWordFeatures(poem, featureVector)

featureVector = averageWordLength(poem, featureVector)

featureVector = poemLength(poem, featureVector)

featureVector = hasSimile(poem, featureVector)

featureVector = hasAlliteration(poem, featureVector, examples, vowels)

featureVector = hasAssonance(poem, featureVector, examples, vowels)

featureVector = averageSentenceLength(poem, featureVector)

print featureVector
"""

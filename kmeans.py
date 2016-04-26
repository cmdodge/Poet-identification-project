#!/usr/bin/python

import random
import collections
import math
import sys
from collections import Counter
from util import *
from pprint import pprint
from feature import *

def kmeans(examples, K, maxIters):
	'''
	examples: list of examples, each example is a string-to-double dict representing a sparse vector.
	K: number of desired clusters
	maxIters: maximum number of iterations to run for (you should terminate early if the algorithm converges).
	Return: (length K list of cluster centroids,
			list of assignments, (i.e. if examples[i] belongs to centers[j], then assignments[i] = j)
			final reconstruction loss)
	'''
	def euclideanDistance(vec1, vec2):
		sum = dotProduct(vec1, vec1) + dotProduct(vec2, vec2) - 2 * dotProduct(vec1, vec2)
		return math.sqrt(sum)

	centroids = random.sample(examples, K)
	assignments = [0 for i in range(len(examples))]

	#precompute phi(xi) dot phi(xi) for each example    
	exampleDots = [dotProduct(examples[i], examples[i]) for i in range(len(examples))]

	totalIterations = 0

	for iteration in range(maxIters):
		totalLoss = 0

		#precompute uk dot uk for each centroid
		centroidDots = [dotProduct(centroids[i], centroids[i]) for i in range(K)]

		#sort examples to closest centroids
		for j in range(len(examples)):
			#compute closest centroid
			closestCentroid = 0
			distance = math.sqrt(exampleDots[j] + centroidDots[0] - 2 * dotProduct(examples[j], centroids[0]))
			for i in range(1, K):
				newDistance = math.sqrt(exampleDots[j] + centroidDots[i] - 2 * dotProduct(examples[j], centroids[i]))
				if newDistance <= distance:
					closestCentroid = i
					distance = newDistance
			assignments[j] = closestCentroid
			totalLoss += distance * distance

		#update centroids
		newCentroids = [Counter() for i in range(K)]
		numUpdated = 0
		clusterSizes = [0 for i in range(K)]
		for i in range(len(assignments)):
			cluster = assignments[i]
			clusterSizes[cluster] = clusterSizes[cluster] + 1
			increment(newCentroids[cluster], 1, examples[i])
		for i in range(K):
			for key in newCentroids[i].keys():
				newCentroids[i][key] = newCentroids[i][key] / float(clusterSizes[i])
				if newCentroids[i][key] != centroids[i][key]:
					numUpdated += 1
		centroids = newCentroids
		if numUpdated == 0:
			totalIterations = iteration
			break
	print "total iterations %d" % totalIterations
	return (centroids, assignments, totalLoss)

def main():
	authors = ["emily-dickinson", "william-shakespeare"]
	examples = readExamples('cmudict.0.7a.txt')
	vowels = readSymbols('cmudict.0.7a.vowel_symbols .txt')

	allWorks = []
	for author in authors:
		works = readAuthorExamples(author, author)
		allWorks += works
		#allWorks += random.sample(works, 10)
	
	examples2 = []
	for poem, classification in allWorks:
		featureVector = Counter()
		featureVector = iambicPentameterLevel(poem, featureVector)
		#featureVector = hasCaesura(poem, featureVector)
		#featureVector = hasEnjambment(poem, featureVector)
		#featureVector = extractWordFeatures(poem, featureVector)
		#featureVector = metricalPattern(poem, featureVector)
		#featureVector = rhymeScheme(poem, featureVector, examples)
		examples2.append(featureVector)

	centroids, assignments, totalLoss = kmeans(examples2, 2, 100)

	clusters = [Counter() for i in xrange(2)]
	for i in xrange(len(allWorks)):
		index = assignments[i]
		clusters[index][allWorks[i][1]] += 1

	print "Clusters"
	for cluster in clusters:
		print cluster

if __name__ == '__main__':
	main()
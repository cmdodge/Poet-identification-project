import os, random, operator
from pprint import pprint
from collections import Counter

def readAuthorExamples(author, classification):
    '''
    Read each author's works into a list of (poem, author) tuples. Each poem in the tuples is a list of its (string) lines
    '''
    allWorks = []
    posLines = [line.strip() for line in open(author + ".txt")]
    start = 0
    poem = []
    for line in posLines:
        if len(line) > 0 and line[0] == "#":
            allWorks.append((poem, classification))
            poem = []
        else:
            poem.append(line)
    #pprint(allWorks)
    return allWorks

def dotProduct(d1, d2):
    """
    @param dict d1: a feature vector represented by a mapping from a feature (string) to a weight (float).
    @param dict d2: same as d1
    @return float: the dot product between d1 and d2
    """
    if len(d1) < len(d2):
        return dotProduct(d2, d1)
    else:
        return sum(d1.get(f, 0) * v for f, v in d2.items())

def increment(d1, scale, d2):
    """
    Implements d1 += scale * d2 for sparse vectors.
    @param dict d1: the feature vector which is mutated.
    @param float scale
    @param dict d2: a feature vector.
    """
    for f, v in d2.items():
        d1[f] = d1.get(f, 0) + v * scale

def evaluatePredictor(examples, predictor, verbose):
    '''
    predictor: a function that takes an x and returns a predicted y.
    Given a list of examples (x, y), makes predictions based on |predict| and returns the fraction
    of misclassiied examples.
    '''
    error = 0
    for x, y in examples:
        if predictor(x) != y:
            error += 1
            if verbose:
                print "WRONG (expected " + y + ", predicted " + predictor(x) + "): " + x[0]
                #print "WRONG (expected %d): " % y + x[0]
        elif verbose:
            print "CORRECT (predicted " + y + "): " + x[0]
            #print "CORRECT (predicted %d): " % y + x[0]
    return 1.0 * error / len(examples)

def outputWeights(weights, path):
    print "%d weights" % len(weights)
    out = open(path, 'w')
    for f, v in sorted(weights.items(), key=lambda (f, v) : -v):
        print >>out, '\t'.join([f, str(v)])
    out.close()

def outputErrorAnalysis(examples, featureExtractor, weights, path):
    out = open('error-analysis', 'w')
    for x, y in examples:
        print >>out, '===', x
        verbosePredict(featureExtractor(x), y, weights, out)
    out.close()

def interactivePrompt(featureExtractor, weights):
    while True:
        print '> ',
        x = sys.stdin.readline()
        if not x: break
        phi = featureExtractor(x) 
        verbosePredict(phi, None, weights, sys.stdout)

def outputClusters(path, examples, centers, assignments):
    '''
    Output the clusters to the given path.
    '''
    print 'Outputting clusters to %s' % path
    out = open(path, 'w')
    for j in range(len(centers)):
        print >>out, '====== Cluster %s' % j
        print >>out, '--- Centers:'
        for k, v in sorted(centers[j].items(), key = lambda (k,v) : -v):
            if v != 0:
                print >>out, '%s\t%s' % (k, v)
        print >>out, '--- Assigned points:'
        for i, z in enumerate(assignments):
            if z == j:
                print >>out, ' '.join(examples[i].keys())
    out.close()

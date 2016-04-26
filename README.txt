data.zip:
extensive known writing samples for relevant poets
CMU pronunciation dictionary, broken down into 
CMU pronunciation dictionary's phoneme symbol list (complete)
CMU pronunciation dictionary's phoneme symbol list (vowel sounds only)

poemScraper.py:
scrapes the Poetry Foundation website for the complete poetic works of a specified poet
outputs complete works into a .txt file
to run: python poemScraper.py

feature.py:
feature extractors with helper functions

util.py:
contains helper functions for feature vector operations, reading author's works into lists, outputting a classification prediction, outputting weights, outputting error analysis, and outputting clusters for k-means clustering

kmeans.py:
runs k-means clustering on the features provided
to run: python kmeans.py

predictor.py:
performs multi-class classification on a data set of poets and their known works
to run: python predictor.py
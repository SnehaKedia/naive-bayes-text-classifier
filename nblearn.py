#!/usr/bin/env python
# coding: utf-8

# ### Importing all packages

# In[1]:


import sys
import glob
import os
import re
from collections import Counter
import time
import math


# ### Functions for Tokenization

# In[2]:


def removeStopwords(wordList):
    usefulWords = []
    for word in wordList:
        # if word not in stopwords
        if word not in stopwordsHashmap:
            usefulWords.append(word)
    return usefulWords

def getCounter(files):
    countDict = Counter()
    countValues = 0
    for file in files:
        line = open(file, 'r').read()
        line = line.lower()
        line = re.sub(r"[^a-zA-Z]+", ' ', line)
        wordList = line.split()
        wordList = removeStopwords(wordList)
        wordCount = Counter(wordList)
        countDict += wordCount
        countValues += len(wordList)
    return countDict, countValues


# ### Function for Conditional Probability 

# In[3]:


def getConditionalProb(counterDict, countValues):
    denominator = math.log(countValues + totalUniqueWords)
    conditionalProbDict = {}
    for key, value in counterDict.items():
        conditionalProbDict[key] = math.log(value + 1) - denominator
    conditionalProbDict['$DEFAULT'] = math.log(1) - denominator
    return conditionalProbDict


# ### Read Stopwords

# In[4]:


# stopwords = list()
stopwordsHashmap = dict()

with open("stopwords.txt", 'r') as file:
    temp = file.readlines()
    for line in temp:
        word = line.strip()
        # stopwords.append(word)
        stopwordsHashmap[word] = True
    file.close()


# ### Accesing all Files

# In[5]:


pathToInput = sys.argv[1]
# pathToInput = 'op_spam_training_data'

allTextFiles = glob.glob(os.path.join(pathToInput, '*/*/*/*.txt'))

positiveTruthfulFiles = [file for file in allTextFiles if "positive" in file and "truthful" in file]
positiveDeceptiveFiles = [file for file in allTextFiles if "positive" in file and "deceptive" in file]
negativeTruthfulFiles = [file for file in allTextFiles if "negative" in file and "truthful" in file]
negativeDeceptiveFiles = [file for file in allTextFiles if "negative" in file and "deceptive" in file]

totalFilesCount = len(allTextFiles)


# ### Calculating unique occurences and frequencies

# In[6]:


# start = time.time()
PTCounterDict, PTCount = getCounter(positiveTruthfulFiles)
PDCounterDict, PDCount = getCounter(positiveDeceptiveFiles)
NTCounterDict, NTCount = getCounter(negativeTruthfulFiles)
NDCounterDict, NDCount = getCounter(negativeDeceptiveFiles)
# end = time.time()
# print(end - start)

totalUniqueWords = len(PTCounterDict + PDCounterDict + NTCounterDict + NDCounterDict)


# ### Calculating Conditional and Prior Probabilities (Naive Bayes Theorem and Laplace Transformation)

# In[7]:


## Encountered divide by zero error
## Storing prob as log

# start = time.time()

# Conditional Probability
PTCondProbDict = getConditionalProb(PTCounterDict, PTCount)
PDCondProbDict = getConditionalProb(PDCounterDict, PDCount)
NTCondProbDict = getConditionalProb(NTCounterDict, NTCount)
NDCondProbDict = getConditionalProb(NDCounterDict, NDCount)

# Prior Probability
PTPriorProb = math.log(len(positiveTruthfulFiles)) - math.log(totalFilesCount)
PDPriorProb = math.log(len(positiveDeceptiveFiles)) - math.log(totalFilesCount)
NTPriorProb = math.log(len(negativeTruthfulFiles)) - math.log(totalFilesCount)
NDPriorProb = math.log(len(negativeDeceptiveFiles)) - math.log(totalFilesCount)

# end = time.time()
# print(end - start)

# ### Writing into nbmodel file

# In[8]:


with open("nbmodel.txt", 'w') as file:
    
    file.write("PTCondProbDict=" + str(dict(PTCondProbDict)) + "\n")
    file.write("PDCondProbDict=" + str(dict(PDCondProbDict)) + "\n")
    file.write("NTCondProbDict=" + str(dict(NTCondProbDict)) + "\n")
    file.write("NDCondProbDict=" + str(dict(NDCondProbDict)) + "\n")

    file.write("PTPriorProb=" + str(PTPriorProb) + "\n")
    file.write("PDPriorProb=" + str(PDPriorProb) + "\n")
    file.write("NTPriorProb=" + str(NTPriorProb) + "\n")
    file.write("NDPriorProb=" + str(NDPriorProb) + "\n")
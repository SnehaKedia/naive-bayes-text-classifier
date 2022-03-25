#!/usr/bin/env python
# coding: utf-8

# ### Importing all packages

# In[1]:


import sys
import glob
import os
import ast
import re


# ### Functions for Tokenization and Labels

# In[2]:


def removeStopwords(wordList):
    usefulWords = []
    for word in wordList:
        # if word not in stopwords:
        if word not in stopwordsHashmap:
            usefulWords.append(word)
    return usefulWords

def getScore(wordList, condProbDict, priorProb):
    score = priorProb
    for word in wordList:
        if word in condProbDict:
            score += condProbDict[word]
        else:
            score += condProbDict['$DEFAULT']
    return score


def getLabel(PTScore, PDScore, NTScore, NDScore):
    if PTScore > PDScore and PTScore > NTScore and PTScore > NDScore:
        return ('truthful', 'positive')
    elif PDScore > PTScore and PDScore > NTScore and PDScore > NDScore:
        return ('deceptive', 'positive')
    elif NTScore > PTScore and NTScore > PDScore and NTScore > NDScore:
        return ('truthful', 'negative')
    else:
        return ('deceptive', 'negative')

def getPredictions(files):
    outputs = {}
    for file in files:
        line = open(file, 'r').read()
        line = line.lower()
        line = re.sub(r"[^a-zA-Z]+", ' ', line) ## isalphanumeric() works but regex is better in time
        wordList = line.split()
        wordList = removeStopwords(wordList)
        
        PTScore = getScore(wordList, PTCondProbDict, PTPriorProb)
        PDScore = getScore(wordList, PDCondProbDict, PDPriorProb)
        NTScore = getScore(wordList, NTCondProbDict, NTPriorProb)
        NDScore = getScore(wordList, NDCondProbDict, NDPriorProb)
        
        label = getLabel(PTScore, PDScore, NTScore, NDScore)
        outputs[file] = label
    return outputs


# ### Read Stopwords

# In[3]:


# stopwords = list()
stopwordsHashmap = dict()

with open("stopwords.txt", 'r') as file:
    temp = file.readlines()
    for line in temp:
        word = line.strip()
        # stopwords.append(word)
        stopwordsHashmap[word] = True
    file.close()


# ### Accesing Files

# In[4]:


pathToInput = sys.argv[1]
# pathToInput = 'op_spam_training_data'

testFiles = glob.glob(os.path.join(pathToInput, '*/*/*/*.txt'))


# ### Reading model file

# In[5]:


file = open("nbmodel.txt", 'r')
temp = file.readlines()
model = {}
for line in temp:
    (key, value) = line.split('=')
    model[key.strip()] = value.strip()


# In[6]:

# start = time.time()

# Posterior Probability
PTCondProbDict = ast.literal_eval(model.get('PTCondProbDict'))
PDCondProbDict = ast.literal_eval(model.get('PDCondProbDict'))
NTCondProbDict = ast.literal_eval(model.get('NTCondProbDict'))
NDCondProbDict = ast.literal_eval(model.get('NDCondProbDict'))

# Prior Probability
PTPriorProb = float(model.get('PTPriorProb'))
PDPriorProb = float(model.get('PDPriorProb'))
NTPriorProb = float(model.get('NTPriorProb'))
NDPriorProb = float(model.get('NDPriorProb'))

# end = time.time()
# print(end - start)


# ### Writing into nboutput file

# In[7]:


outputs = getPredictions(testFiles)
with open("nboutput.txt", 'w') as file:
    for fileName, prediction in outputs.items():
        file.write(prediction[0] + ' ' + prediction[1] + ' ' + fileName + '\n')
    file.close()
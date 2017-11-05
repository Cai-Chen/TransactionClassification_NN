# -*- coding: utf-8 -*-
import numpy as np
import json
import vocabulary

class InputData(object):
    def __init__(self, trainDir, testDir, vocabDir, cateDir):
        self.trainDir = trainDir
        self.testDir = testDir
        self.vocab = vocabulary.Vocabulary()
        self.load_train = None
        self.load_test = None
        self.load_category = None
        self.trainingData = []
        self.trainingLabel = []
        self.testingData = []
        self.batch_train_idx = 0
        self.batch_test_idx = 0

        # Initial the vocabulary list
        for dir in vocabDir:
            self.vocab.getVocab(dir)
        self.vocab.getIdx()

        # Open the category file
        with open(cateDir, 'r', encoding='utf-8') as load_f:
             self.load_category = json.load(load_f)

    def getTrainDataAndLabel(self):
        # Vocabulary list length
        length = len(self.vocab.vocab)
        # Read the training data
        with open(self.trainDir, 'r', encoding='utf-8') as load_f:
             self.load_train = json.load(load_f)
             for card in self.load_train:
                 # Get vector for data
                 description = card['title']
                 descRep = np.zeros(length, dtype=float)
                 for word in description.split(' '):
                     descRep[self.vocab.word2index[word.lower()]] += 1
                 self.trainingData.append(descRep)
                 # Get vector for label
                 category = card['category']
                 # Add 'GENERAL' as the default category
                 cateRep = np.zeros(len(self.load_category) + 1, dtype=float)
                 for i in range(0, len(self.load_category)):
                     if self.load_category[i]['category'] == category:
                         cateRep[i] = 1
                 if category == 'GENERAL':
                     cateRep[len(self.load_category)] = 1
                 self.trainingLabel.append(cateRep)

    def get_train_batch(self, batch_size):
        batch_data = None
        if self.batch_train_idx + batch_size <= len(self.trainingData):
            batch_data = np.array(self.trainingData[self.batch_train_idx : self.batch_train_idx + batch_size]), np.array(self.trainingLabel[self.batch_train_idx : self.batch_train_idx + batch_size])
            self.batch_train_idx += batch_size
        return batch_data

    def getTestData(self):
        # Vocabulary list length
        length = len(self.vocab.vocab)
        # Read the testing data
        with open(self.testDir, 'r', encoding='utf-8') as load_f:
             self.load_test = json.load(load_f)
             for card in self.load_test:
                 # Get vector for data
                 description = card['title']
                 descRep = np.zeros(length, dtype=float)
                 for word in description.split(' '):
                     descRep[self.vocab.word2index[word.lower()]] += 1
                 self.testingData.append(descRep)

    def get_test_batch(self, batch_size):
        batch_data = None
        if self.batch_test_idx + batch_size <= len(self.trainingData):
            batch_data = np.array(self.testingData[self.batch_test_idx : self.batch_test_idx + batch_size])
            self.batch_test_idx += batch_size
        return batch_data

    def get_category_byID(self, id):
        return 'GENERAL' if id >= len(self.load_category) else self.load_category[id]['category']

    def storeData(self):
        print (len(self.trainingData))
        print (len(self.trainingLabel))
        for _ in range(100):
            with open('./test.txt', 'a', encoding='utf-8') as dump_f:
                # json.dump(self.trainingData, dump_f)
                dump_f.write(str(self.get_batch(100)))

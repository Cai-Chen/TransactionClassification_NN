import json
from collections import Counter

class Vocabulary(object):
    def __init__(self):
        # Vocabulary list
        self.vocab = Counter()
        # Word index list
        self.word2index = {}

    def getVocab(self, readDir):
        # Initial the vocabulary list
        with open(readDir, 'r', encoding='utf-8') as load_f:
            load_json = json.load(load_f)
            for card in load_json:
                description = card['title']
                for word in description.split(' '):
                    word_lowercase = word.lower()
                    self.vocab[word_lowercase] += 1

    def getIdx(self):
        # Initial the index of the word in the vocabulary list
        for i,word in enumerate(self.vocab):
            self.word2index[word] = i

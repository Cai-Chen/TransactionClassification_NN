# -*- coding: utf-8 -*-

import json
import re

class Classification(object):

    def __init__(self, cateDir, readDir, writeDir):
        self.cateDir = cateDir
        self.readDir = readDir
        self.writeDir = writeDir
        self.load_json = None
        self.load_category = None
        self.write_json = []

        # Open the category file
        with open(cateDir, 'r', encoding='utf-8') as load_f:
             self.load_category = json.load(load_f)

    def cleanData(self):
        with open(self.readDir, 'r', encoding='utf-8') as load_f:
            self.load_json = json.load(load_f)
            for card in self.load_json:
                # Remove the string with .
                match = re.match(r'(.*)\s+(.*\..*)', card['title'])
                if match:
                    card['title'] = match.group(1)
                # Remove the string after mutiplie space
                match = re.match(r'(.*?)\s{2,}(.*)', card['title'])
                if match:
                    card['title'] = match.group(1)
                # Remove the string with -
                match = re.match(r'(.*)\s+(.*\-.*)', card['title'])
                if match:
                    card['title'] = match.group(1)
                # Remove the string with :
                match = re.match(r'(.*\:.*?)\s{2,}(.*)', card['title'])
                if match:
                    card['title'] = match.group(2)

                # Update category
                card['category'] = self.categorize(card['title'])

                # Write
                self.write_json.append({'category' : card['category'], "title" : card['title']})

                # print (card['title'].encode('utf8'))

    def categorize(self, title):
        # Find the category
        for i in range(0, len(self.load_category)):
            for j in range(0, len(self.load_category[i]['tags'])):
                if self.load_category[i]['tags'][j].upper() in title.upper():
                    return self.load_category[i]['category']
        # If not found, return GENERAL
        return 'GENERAL'

    def storeData(self):
        with open(self.writeDir, 'w', encoding='utf-8') as dump_f:
            json.dump(self.write_json, dump_f)

if __name__ == '__main__':
    classify = Classification('./category.json', './rawData.json', './trainingData.json')
    classify.cleanData()
    classify.storeData()

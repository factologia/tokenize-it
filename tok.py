from xml.etree import ElementTree as ET
from os import listdir as ls
from os.path import isfile, isdir, join
from fnmatch import fnmatch
import re
import grmodel
import itertools
import random

import logging

log = logging.getLogger(__name__)

class Tok:
    def __init__(self, dict):
        self.dict = dict
        self.sep = re.compile('[^\w]+')
        self.boom_protection = False

    def enable_boom_protection(self):
        self.boom_protection = True

    def words(self, text):
        res = []
        for i in range(1, len(text) + 1):
            token = text[:i]
            if token in self.dict.keys():
                res.append([token, text[i:]])
        return res

    def fuzzytok(self, text, limit=None):
        text.lower()
        res = []
        queue = self.words(text)
        while queue:
            seq = queue.pop(random.randrange(len(queue)))
            tail = seq.pop()
            if tail:
                for s in self.words(tail):
                    queue = queue + [seq + s]
            else:
                res.append(seq)
            if limit:
                if len(res) >= limit:
                    break
        return res

    def tok(self, text, gr=False, fuzzylimit=None):
        res = []
        for t in self.sep.split(text):
            if t in self.dict.keys():
                res.append([[t]])
            else:
                res.append(self.fuzzytok(t, fuzzylimit))
        res = [[j for i in r for j in i] for r in itertools.product(*res)]
        if gr:
            return self.addgr_to_sentences(res)
        else:
            return res

    def addgr(self, sentence):
        res = []
        size = 1;
        for word in sentence:
            entries = self.dict[word]
            size = size * len(entries)
            res.append(entries)
        if self.boom_protection and size > 10000:
            #log.debug("size is %i", size)
            #log.warn("boom for sentence %s", str(sentence))
            return []
        else:
            return [x for x in itertools.product(*res)]

    def addgr_to_sentences(self, snts):
        return [j for i in [self.addgr(s) for s in snts] for j in i]

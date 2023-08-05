#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Using `regex` instead of Python built-in `re` module.

"""
import regex as re
from Levenshtein import distance
import time
import csv

"""Constant declaration
"""
MAX_RESULT = 20
DEF_INPUT_FILE = 'deduped_augmented_clean_names.csv'
RESULT_FIELDS = ['uniqid', 'n', 'match', 'start', 'end']

class SearchMultipleKeywords(object):
    """Search by multiple keywords list
    """
    def __init__(self, keywords, fuzzy_min_len=None):
        """Initialize search
        """
        if fuzzy_min_len is None:
            fuzzy_min_len = []
        self.fuzzy_min_len = sorted(fuzzy_min_len)
        self.keywords = {}
        for i, k in keywords:
            if i not in self.keywords:
                self.keywords[i] = [k.strip().lower()]
            else:
                self.keywords[i].append(k.strip().lower())

        print("Number of unique keywords ID to be searched: {0}"
              .format(len(self.keywords)))

        self.re_keywords = dict()
        for i in self.keywords:
            kw = []
            for k in self.keywords[i]:
                d = self.get_allow_distance(k)
                if d:
                    kw.append(r'(?:{0}){{e<={1}}}'.format(re.escape(k), d))
                else:
                    kw.append(re.escape(k))
            re_str = '|'.join(kw)
            re_str = r'\b(?:{0})\b'.format(re_str)
            self.re_keywords[i] = re.compile(re_str, flags=re.I)

    def get_allow_distance(self, k):
        dist = 0
        for l, d in self.fuzzy_min_len:
            if len(k) > l:
                dist = d
        return dist

    def search(self, s, n=MAX_RESULT):
        """Search
        """
        c = []
        if n == 0:
            return c

        match = dict()
        for k in self.re_keywords:
            for a in self.re_keywords[k].finditer(s):
                name = a.group(0).strip()
                if k in match:
                    match[k].append((name, a.start(0), a.end(0)))
                else:
                    match[k] = [(name, a.start(0), a.end(0))]

        j = 0
        for k in match:
            c.extend([k, len(match[k]), ';'.join([m[0] for m in match[k]]),
                      ';'.join([str(m[1]) for m in match[k]]),
                      ';'.join([str(m[2]) for m in match[k]])])
            j += 1
            if j >= n:
                break
        while j < n:
            for a in RESULT_FIELDS:
                c.append('')
            j += 1
        count = 0
        for m in match:
            count += len(match[m])

        return c, count


class NewSearchMultipleKeywords(object):
    """New search by multiple keywords (should be faster if large keywords)
    """

    def __init__(self, keywords, fuzzy_min_len=None):
        """Initialize search
        """
        if fuzzy_min_len is None:
            fuzzy_min_len = []
        self.fuzzy_min_len = sorted(fuzzy_min_len)
        self.keywords = {}
        for i, k in keywords:
            k = k.strip().lower()
            if k not in self.keywords:
                self.keywords[k] = i
            else:
                print("ERROR: found duplicate keyword '{0}'".format(k))

        print("Number of unique keywords ID to be searched: {0}"
              .format(len(self.keywords)))

        kw = []
        for k in self.keywords:
            d = self.get_allow_distance(k)
            if d:
                kw.append(r'(?:{0}){{e<={1}}}'.format(re.escape(k), d))
            else:
                kw.append(re.escape(k))

        re_str = '|'.join(kw)
        re_str = r'\b(?:{0})\b'.format(re_str)
        self.re_keywords = re.compile(re_str)

    def get_allow_distance(self, k):
        dist = 0
        for l, d in self.fuzzy_min_len:
            if len(k) > l:
                dist = d
        return dist

    def find_nearest_key(self, key):
        for k in self.keywords:
            d = self.get_allow_distance(k)
            if distance(k, key) <= d:
                return k

    def search(self, s, n=MAX_RESULT):
        """Search
        """
        c = []
        if n == 0:
            return c

        j = 0
        match = dict()
        for a in self.re_keywords.finditer(s):
            fkey = a.group(0).strip()
            if fkey not in self.keywords:
                fkey = a.group(0)
                nearestkey = self.find_nearest_key(fkey)
                #print("Approximate match '%s' ==> '%s'" % (fkey, nearestkey))
                key = nearestkey
            else:
                key = fkey
            rowid = self.keywords[key]
            if rowid in match:
                match[rowid].append((fkey, a.start(0), a.end(0)))
            else:
                match[rowid] = [(fkey, a.start(0), a.end(0))]

        j = 0
        for k in match:
            c.extend([k, len(match[k]), ';'.join([m[0] for m in match[k]]),
                      ';'.join([str(m[1]) for m in match[k]]),
                      ';'.join([str(m[2]) for m in match[k]])])
            j += 1
            if j >= n:
                break
        while j < n:
            for a in RESULT_FIELDS:
                c.append('')
            j += 1
        count = 0
        for m in match:
            count += len(match[m])

        return c, count


if __name__ == "__main__":
    

    keywords = []
    with open(DEF_INPUT_FILE, 'rb') as f:
        reader = csv.DictReader(f)
        for r in reader:
            keywords.append((r['uniqid'], r['search_name']))

    n_result = 5
    search_obj = SearchMultipleKeywords(keywords, [(10, 1), (15, 2)])
    out = open('tests/output-1.csv', 'wb')
    writer = csv.writer(out)
    with open('tests/text_corpus.csv', 'rb') as f:
        reader = csv.DictReader(f)
        result_header = reader.fieldnames
        for i in range(0, n_result):
            for j in RESULT_FIELDS:
                result_header.append('name{0}.{1}'.format(i + 1, j))
        result_header.append('count')
        writer.writerow(result_header)
        start_time = time.time()
        for i, r in enumerate(reader):
            uid = r['uniqid']
            text = r['text']
            c = [uid, text]
            result, count = search_obj.search(text, n_result)
            c.extend(result)
            c.append(count)
            writer.writerow(c)
        elaspe = time.time() - start_time
        print("Average rate = {0:f} rows/min".format((i * 60 / elaspe)))
    out.close()

    # Test new search
    n_result = 5
    search_obj = NewSearchMultipleKeywords(keywords, [(10, 1), (15, 2)])
    out = open('tests/output-2.csv', 'wb')
    writer = csv.writer(out)
    with open('tests/text_corpus.csv', 'rb') as f:
        reader = csv.DictReader(f)
        result_header = reader.fieldnames
        for i in range(0, n_result):
            for j in RESULT_FIELDS:
                result_header.append('name{0}.{1}'.format(i + 1, j))
        result_header.append('count')
        writer.writerow(result_header)
        start_time = time.time()
        for i, r in enumerate(reader):
            uid = r['uniqid']
            text = r['text']
            c = [uid, text]
            result, count = search_obj.search(text, n_result)
            c.extend(result)
            c.append(count)
            writer.writerow(c)
        elaspe = time.time() - start_time
        print("Average rate = {0:f} rows/min".format((i * 60 / elaspe)))
    out.close()

#!/usr/bin/env python

import cPickle
import cv2
from imageSearchEngine import Searcher
import argparse

"""
This script provides a interface to query over the image search engine
"""

__author__ = 'Shaun Rong'
__version__ = '0.1'
__maintainer__ = 'Shaun Rong'
__email__ = 'rongzq08@gmail.com'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-q', required=True, help='path to the image used as a query')
    parser.add_argument('-n', type=int, required=True, help='show the first n results')
    args = parser.parse_args()

    index = cPickle.loads(open('index.pkl').read())
    searcher = Searcher(index)
    query = args.q[args.q.rfind('/')+1:]
    results = searcher.search(index[query])

    query_image = cv2.imread(args.q)
    cv2.imshow('Query', query_image)

    for j in range(args.n):
        (score, image_name) = results[j]
        path = 'images/{}'.format(image_name)
        result = cv2.imread(path)
        cv2.imshow('Results {}'.format(j), result)
        cv2.waitKey(0)
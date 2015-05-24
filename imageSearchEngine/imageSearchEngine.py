#!/usr/bin/env python
import cv2
import numpy as np

__author__ = 'Shaun Rong'
__version__ = '0.1'
__maintainer__ = 'Shaun Rong'
__email__ = 'rongzq08@gmail.com'


class RGBHistogram:
    def __init__(self, bins):
        self._bins = bins

    def describe(self, image):
        hist = cv2.calcHist([image], [0, 1, 2], None, self._bins, [0, 256, 0, 256, 0, 256])
        hist = cv2.normalize(hist)
        return hist.flatten()


class Searcher:
    def __init__(self, index):
        self._index = index

    def search(self, query_features):
        results = {}
        for (k, features) in self._index.items():
            d = self.chi2_distance(features, query_features)
            results[k] = d
        results = sorted([(v, k) for (k, v) in results.items()])
        return results

    @staticmethod
    def chi2_distance(hist_A, hist_B, eps=1e-10):
        d = 0.5 * np.sum([((a - b) ** 2) / (a + b + eps) for (a, b) in zip(hist_A, hist_B)])
        return d
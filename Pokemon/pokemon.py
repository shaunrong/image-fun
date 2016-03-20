#!/usr/bin/env python

__author__ = 'Shaun Rong'
__version__ = '0.1'
__maintainer__ = 'Shaun Rong'
__email__ = 'rongzq08@gmail.com'

import mahotas
from scipy.spatial import distance as dist


class ZernikeMoments:
    def __init__(self, radius):
        self._radius = radius

    def describe(self, image):
        return mahotas.features.zernike_moments(image, self._radius)


class Searcher:
    def __init__(self, index):
        self._index = index

    def search(self, query_feautres):
        results = {}
        for (k, features) in self._index.items():
            d = dist.euclidean(query_feautres, features)
            results[k] = d

        results = sorted([(v, k) for (k, v) in results.items()])

        return results

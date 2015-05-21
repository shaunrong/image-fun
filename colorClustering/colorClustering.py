#!/usr/bin/env python
import argparse
import cv2
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import numpy as np

__author__ = 'Shaun Rong'
__version__ = '0.1'
__maintainer__ = 'Shaun Rong'
__email__ = 'rongzq08@gmail.com'


def color_clustering(image, clusters):
    """
    clustering the main colors in a picture with KMeans algorithm.
    example: run "python colorClustering.py -i 'tuotuo.JPG' -c 6"
    :param image: file path
    :param clusters: number of clusters in that picture
    :return: tow images shown using matplotlib
    """
    img = cv2.imread(image)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    plt.figure()
    plt.axis('off')
    plt.imshow(img)

    img = img.reshape((img.shape[0] * img.shape[1], 3))
    clt = KMeans(n_clusters=clusters)
    clt.fit(img)

    hist = centroid_histogram(clt)
    bar = plot_colors(hist, clt.cluster_centers_)

    plt.figure()
    plt.axis('off')
    plt.imshow(bar)
    plt.show()


def centroid_histogram(clt):
    numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
    (hist, _) = np.histogram(clt.labels_, bins=numLabels)
    hist = hist.astype('float')
    hist /= hist.sum()
    return hist


def plot_colors(hist, centroid):
    bar = np.zeros((50, 300, 3), dtype='uint8')
    startX = 0

    for (percent, color) in zip(hist, centroid):
        endX = startX + (percent * 300)
        cv2.rectangle(bar, (int(startX), 0), (int(endX), 50), color.astype('uint8').tolist(), -1)
        startX = endX

    return bar

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', type=str, required=True, help='path to the image')
    parser.add_argument('-c', type=int, required=True, help='# of clusters')

    args = parser.parse_args()

    color_clustering(args.i, args.c)



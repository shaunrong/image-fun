#!/usr/bin/env python
import cv2
import matplotlib.pyplot as plt

__author__ = 'Shaun Rong'
__version__ = '0.1'
__maintainer__ = 'Shaun Rong'
__email__ = 'rongzq08@gmail.com'

image = cv2.imread('grant.jpg')
cv2.imshow('image', image)
chans = cv2.split(image)
colors = ('b', 'g', 'r')
plt.figure()
plt.title("'Flattened' Color Histogram")
plt.xlabel('Bins')
plt.ylabel('# of Pixels')
plt.xlim([0, 256])
features = []

for (chan, color) in zip(chans, colors):
    hist = cv2.calcHist([chan], [0], None, [256], [0,256])
    features.extend(hist)
    plt.plot(hist, color=color)

plt.show()


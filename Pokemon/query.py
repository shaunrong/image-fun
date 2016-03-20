#!/usr/bin/env python
import cPickle
import cv2
import numpy as np
from skimage import exposure
from pokemon import ZernikeMoments, Searcher

__author__ = 'Shaun Rong'
__version__ = '0.1'
__maintainer__ = 'Shaun Rong'
__email__ = 'rongzq08@gmail.com'


def poke_query(image):
    image = cv2.imread(image)
    ratio = image.shape[0] / 400.0
    orig = image.copy()
    image = cv2.resize(image, (int(image.shape[1] / ratio), 400), interpolation=cv2.INTER_AREA)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    edged = cv2.Canny(gray, 30, 200)

    (cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:10]
    screen_cnt = None

    for i, c in enumerate(cnts):
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.01 * peri, True)
        #image_copy = image.copy()
        #cv2.drawContours(image_copy, [approx], -1, (0, 255, 0), 3)
        #cv2.imshow('contour {}'.format(i), image_copy)
        #cv2.waitKey(0)
        #print len(approx)
        if len(approx) == 4:
            screen_cnt = approx
            break

    pts = screen_cnt.reshape(4, 2)
    rect = np.zeros((4, 2), dtype='float32')
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    rect *= ratio

    (tl, tr, br, bl) = rect
    widthA = np.sqrt((br[0] - bl[0]) ** 2 + (br[1] - bl[1]) ** 2)
    widthB = np.sqrt((tr[0] - tl[0]) ** 2 + (tr[1] - tl[1]) ** 2)

    heightA = np.sqrt((tr[0] - br[0]) ** 2 + (tr[1] - br[1]) ** 2)
    heightB = np.sqrt((tl[0] - bl[0]) ** 2 + (tl[1] - bl[1]) ** 2)

    max_width = max(int(widthA), int(widthB))
    max_height = max(int(heightA), int(heightB))

    dst = np.array([[0, 0], [max_width - 1, 0], [max_width - 1, max_height - 1], [0, max_height - 1]], dtype='float32')

    M = cv2.getPerspectiveTransform(rect, dst)
    warp = cv2.warpPerspective(orig, M, (max_width, max_height))

    warp = cv2.cvtColor(warp, cv2.COLOR_BGR2GRAY)
    warp = exposure.rescale_intensity(warp, out_range=(0, 255))

    (h, w) = warp.shape
    (dX, dY) = (int(w * 0.4), int(h * 0.45))
    crop = warp[10:dY, w - dX:w - 10]

    crop_resize_ratio = 64.0 / crop.shape[1]
    crop = cv2.resize(crop, (64, int(crop.shape[0] * crop_resize_ratio)), interpolation=cv2.INTER_AREA)
    thresh = cv2.adaptiveThreshold(crop, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 7)
    outline = np.zeros(crop.shape, dtype='uint8')
    (cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[0]
    cv2.drawContours(outline, [cnts], -1, 255, -1)

    desc = ZernikeMoments(21)
    query_feature = desc.describe(outline)

    with open('index.pkl', 'r') as f:
        index = cPickle.loads(f.read())
    searcher = Searcher(index)
    results = searcher.search(query_feature)
    for i in range(5):
        print results[i][1]

    """
    cv2.drawContours(image, [screen_cnt], -1, (0, 255, 0), 3)
    cv2.imshow('screen', image)
    cv2.waitKey(0)
    """

if __name__ == '__main__':
    poke_query('query_marowak.jpg')
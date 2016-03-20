#!/usr/bin/env python

__author__ = 'Shaun Rong'
__version__ = '0.1'
__maintainer__ = 'Shaun Rong'
__email__ = 'rongzq08@gmail.com'

from pokemon import ZernikeMoments
import glob
import cv2
import numpy as np
import os
import cPickle


def main():
    desc = ZernikeMoments(21)
    index = {}

    for path in glob.glob('img/*.jpg'):
        pokemon = path[path.rfind("/") + 1:].replace('.jpg', '')
        try:
            image = cv2.imread(path)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            image = cv2.copyMakeBorder(image, 15, 15, 15, 15, cv2.BORDER_CONSTANT, value=255)
            thresh = cv2.bitwise_not(image)
            thresh[thresh > 0] = 255
            outline = np.zeros(image.shape, dtype='uint8')
            (cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[0]
            cv2.drawContours(outline, [cnts], -1, 255, -1)
            moments = desc.describe(outline)
            index[pokemon] = moments
        except:
            os.remove(path)

    with open('index.pkl', 'w') as f:
        f.write(cPickle.dumps(index))

if __name__ == '__main__':
    main()
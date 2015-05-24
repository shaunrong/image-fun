#!/usr/bin/env python
import glob
import cPickle
import cv2
from imageSearchEngine import RGBHistogram

__author__ = 'Shaun Rong'
__version__ = '0.1'
__maintainer__ = 'Shaun Rong'
__email__ = 'rongzq08@gmail.com'


def main():
    index = {}
    desc = RGBHistogram([8, 8, 8])

    for image_path in (glob.glob('images/*.jpeg') + glob.glob('images/*.jpg')):
        k = image_path[image_path.rfind("/") + 1:]
        image = cv2.imread(image_path)
        features = desc.describe(image)
        index[k] = features

    with open('index.pkl', 'w') as f:
        f.write(cPickle.dumps(index))


if __name__ == '__main__':
    main()
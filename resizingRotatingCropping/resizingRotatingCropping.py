#!/usr/bin/env python

__author__ = 'Shaun Rong'
__version__ = '0.1'
__maintainer__ = 'Shaun Rong'
__email__ = 'rongzq08@gmail.com'

import cv2


def show_original_image(image):
    cv2.imshow('origin', image)


def show_resized_image(image):
    r = 100.0 / image.shape[1]
    dim = (100, int(r * image.shape[0]) )
    resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    cv2.imshow('resized', resized)


def show_rotated_image(image):
    (h, w) = image.shape[:2]
    center = (w / 2, h / 2)
    M = cv2.getRotationMatrix2D(center, 180, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h))
    cv2.imshow('rotated', rotated)


def show_cropped_image(image):
    cropped = image[70:170, 440:540]
    cv2.imshow('cropped', cropped)
    cv2.imwrite('thumbnail.png', cropped)

if __name__ == '__main__':
    image = cv2.imread('jurassic-park-tour-jeep.jpg')
    show_original_image(image)
    cv2.waitKey(0)
    show_resized_image(image)
    cv2.waitKey(0)
    show_rotated_image(image)
    cv2.waitKey(0)
    show_cropped_image(image)
    cv2.waitKey(0)
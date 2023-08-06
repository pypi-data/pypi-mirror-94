#!/usr/bin/env python
'''
Created by Seria at 02/11/2018 3:38 PM
Email: zzqsummerai@yeah.net

                    _ooOoo_
                  o888888888o
                 o88`_ . _`88o
                 (|  0   0  |)
                 O \   。   / O
              _____/`-----‘\_____
            .’   \||  _ _  ||/   `.
            |  _ |||   |   ||| _  |
            |  |  \\       //  |  |
            |  |    \-----/    |  |
             \ .\ ___/- -\___ /. /
         ,--- /   ___\<|>/___   \ ---,
         | |:    \    \ /    /    :| |
         `\--\_    -. ___ .-    _/--/‘
   ===========  \__  NOBUG  __/  ===========
   
'''
# -*- coding:utf-8 -*-
import math
import numpy as np
import random as rand
from tensorflow import image as tfimg
import tensorflow as tf
from ..toolkit import byte2arr
import scipy.ndimage as ndimage


__all__ = ('Comburant', 'HWC2CHW', 'Random',
           'NEAREST', 'LINEAR', 'CUBIC', 'HORIZONTAL', 'VERTICAL',
           'Resize', 'Crop', 'Flip', 'Rotate',
           'Brighten', 'Contrast', 'Saturate', 'Hue')


NEAREST = 0
LINEAR = 1
CUBIC = 2

TF_INTERP = {NEAREST: 'nearest', LINEAR: 'bilinear', CUBIC: 'bicubic'}
SP_INTERP = {NEAREST: 0, LINEAR: 1, CUBIC: 3}

HORIZONTAL = 10
VERTICAL = 11




class Comburant(object):
    def __init__(self, *args, is_encoded=False):
        self.comburant = list(args)
        self.is_encoded = is_encoded

    def __call__(self, img):
        if self.is_encoded:
            # img = byte2arr(img)
            img = tfimg.decode_jpeg(img)
            img = tf.image.convert_image_dtype(img, tf.float32)
        for cbr in self.comburant:
            img = cbr(img)
        if not tf.is_tensor(img):
            img = tf.convert_to_tensor(img)
        return img



class HWC2CHW(object):
    def __init__(self):
        pass

    def __call__(self, img):
        return tf.transpose(img, (2, 0, 1))



class Random(object):
    def __init__(self, p, comburant):
        self.p = p
        self.cbr = comburant

    def __call__(self, img):
        if rand.random() < self.p:
            return self.cbr(img)
        else:
            return img



class Resize(object):
    def __init__(self, size, interp=LINEAR):
        # size: (height, width)
        self.size = size
        self.interp = interp

    def __call__(self, img):
        return tfimg.resize(img, self.size, TF_INTERP[self.interp])



class Crop(object):
    def __init__(self, size: tuple, padding=(0, 0, 0, 0), area_ratio=(1, 1), aspect_ratio=(1, 1), interp=LINEAR):
        # size: (height, width)
        # padding: (left, top, right, bottom)
        self.size = size
        self.padding = padding
        self.area_ratio = area_ratio
        self.aspect_ratio = aspect_ratio
        self.interp = interp

    def __call__(self, img):
        h, w, c = img.shape
        l, t, r, b = self.padding
        _h = max(h + t + b, self.size[0])
        _w = max(w+l+r, self.size[1])
        img = tfimg.pad_to_bounding_box(img, t, l, _h, _w)
        h = _h
        w = _w

        if self.area_ratio == self.aspect_ratio == (1, 1):
            x = int(rand.random() * (w - self.size[1] + 1))
            y = int(rand.random() * (h - self.size[0] + 1))
            img = img[y:y+self.size[0], x:x+self.size[1]]
        else:
            sqrt_aspect_ratio = math.sqrt(rand.random()
                                          * (self.aspect_ratio[1] - self.aspect_ratio[0]) + self.aspect_ratio[0])
            sqrt_area_ratio = math.sqrt(rand.random()
                                        * (self.area_ratio[1] - self.area_ratio[0]) + self.area_ratio[0])
            cols = int(sqrt_area_ratio * w * sqrt_aspect_ratio)
            rows = int(sqrt_area_ratio * h / sqrt_aspect_ratio)
            x = int(rand.random() * (w - cols + 1))
            y = int(rand.random() * (h - rows + 1))
            img = tfimg.resize(img[y:y+rows, x:x+cols], self.size, TF_INTERP[self.interp])
        return img



class Flip(object):
    def __init__(self, axial):
        self.axial = axial

    def __call__(self, img):
        if self.axial == HORIZONTAL:
            img = tfimg.flip_up_down(img)
        elif self.axial == VERTICAL:
            img = tfimg.flip_left_right(img)
        else:
            raise Exception('NEBULAE ERROR ⨷ the invoked flip type is not defined or supported.')
        return img



class Rotate(object):
    def __init__(self, degree, intact=False, interp=NEAREST):
        '''
        Args
        intact: whether to keep image intact which might enlarge the output size
        '''
        self.degree = degree
        self.intact = intact
        self.interp = interp

    def call(self, img):
        degree = self.degree * (rand.random() * 2 - 1)
        return ndimage.rotate(img, degree, reshape=self.intact, order=SP_INTERP[self.interp])

    # def call(self, img):
    #     h, w, c = img.shape
    #     rot_center = (w / 2., h / 2.)
    #     degree = self.degree * (rand.random() * 2 - 1)
    #     angle = math.radians(degree)
    #     matrix = [
    #         round(math.cos(angle), 15), round(math.sin(angle), 15), 0.,
    #         round(-math.sin(angle), 15), round(math.cos(angle), 15), 0.,
    #     ]
    #
    #     def transform(x, y, matrix):
    #         (a, b, c, d, e, f) = matrix
    #         return a * x + b * y + c, d * x + e * y + f
    #
    #     matrix[2], matrix[5] = transform(-rot_center[0], -rot_center[1], matrix)
    #     matrix[2] += rot_center[0]
    #     matrix[5] += rot_center[1]
    #
    #     if self.intact:
    #         # calculate output size
    #         xx = []
    #         yy = []
    #         for x, y in ((0, 0), (w, 0), (w, h), (0, h)):
    #             x, y = transform(x, y, matrix)
    #             xx.append(x)
    #             yy.append(y)
    #         nw = math.ceil(max(xx)) - math.floor(min(xx))
    #         nh = math.ceil(max(yy)) - math.floor(min(yy))
    #
    #         # We multiply a translation matrix from the right.  Because of its
    #         # special form, this is the same as taking the image of the
    #         # translation vector as new translation vector.
    #         matrix[2], matrix[5] = transform(-(nw - w) / 2.0, -(nh - h) / 2.0, matrix)
    #     else:
    #         nw, nh = w, h
    #
    #     rot_img = np.zeros((nh, nw, c), dtype=img.dtype)
    #     zeros = np.zeros((c,), dtype=img.dtype)
    #     for i in range(nh):
    #         for j in range(nw):
    #             x, y = transform(j, i, matrix)
    #             x, y = round(x), round(y)
    #             if x >= w or y >= h or x < 0 or y < 0:
    #                 pix = zeros
    #             else:
    #                 pix = img[round(y), round(x)]
    #             rot_img[i, j] = pix
    #
    #     return rot_img

    def __call__(self, img):
        shape = img.shape
        img = tf.numpy_function(self.call, [img], tf.float32)
        img.set_shape(shape)
        return img



class Brighten(object):
    def __init__(self, range):
        self.range = range

    def __call__(self, img):
        return tfimg.random_brightness(img, self.range)



class Contrast(object):
    def __init__(self, range):
        self.range = range

    def __call__(self, img):
        return tfimg.random_contrast(img, max(0, 1-self.range), 1+self.range)



class Saturate(object):
    def __init__(self, range):
        self.range = range

    def __call__(self, img):
        return tfimg.random_saturation(img, max(0, 1-self.range), 1+self.range)



class Hue(object):
    def __init__(self, range):
        self.range = range

    def __call__(self, img):
        return tfimg.random_hue(img, self)
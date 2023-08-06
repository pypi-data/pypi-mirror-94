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
import numpy as np
import random as rand
from torchvision.transforms import *
F = functional
from PIL import Image

from ..toolkit import byte2arr


__all__ = ('Comburant', 'HWC2CHW', 'Random',
           'NEAREST', 'LINEAR', 'CUBIC', 'HORIZONTAL', 'VERTICAL',
           'Resize', 'Crop', 'Flip', 'Rotate',
           'Brighten', 'Contrast', 'Saturate', 'Hue')


NEAREST = 0
LINEAR = 1
CUBIC = 2

PIL_INTERP = {NEAREST: Image.NEAREST, LINEAR: Image.BILINEAR, CUBIC: Image.BICUBIC}

HORIZONTAL = 10
VERTICAL = 11




class Comburant(object):
    def __init__(self, *args, is_encoded=False):
        self.comburant = Compose(list(args))
        self.is_encoded = is_encoded

    def __call__(self, img):
        if self.is_encoded:
            img = byte2arr(img, as_np=False)
        img = self.comburant(img)
        img = np.array(img)
        img = img.astype(np.float32) / 255
        return img



class HWC2CHW(object):
    def __init__(self):
        pass

    def __call__(self, img):
        return np.transpose(img, (2, 0, 1))



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
        return img.resize((self.size[1], self.size[0]), PIL_INTERP[self.interp])



class Crop(object):
    def __init__(self, size, padding=(0, 0, 0, 0), area_ratio=(1, 1), aspect_ratio=(1, 1), interp=LINEAR):
        # size: (height, width)
        # padding: (left, top, right, bottom)
        self.size = size
        self.padding = padding
        self.area_ratio = area_ratio
        self.aspect_ratio = aspect_ratio
        if area_ratio == aspect_ratio == (1,1):
            self.comburant = RandomCrop(size)
        else:
            self.comburant = RandomResizedCrop(size, area_ratio, aspect_ratio, PIL_INTERP[interp])

    def __call__(self, img):
        img = F.pad(img, self.padding, 0, 'constant')
        # pad the width if needed
        if img.size[0] < self.size[1]:
            img = F.pad(img, (self.size[1] - img.size[0], 0), 0, 'constant')
        # pad the height if needed
        if img.size[1] < self.size[0]:
            img = F.pad(img, (0, self.size[0] - img.size[1]), 0, 'constant')
        return self.comburant(img)



class Flip(object):
    def __init__(self, axial):
        if axial == HORIZONTAL:
            self.comburant = RandomVerticalFlip(1)
        elif axial == VERTICAL:
            self.comburant = RandomHorizontalFlip(1)
        else:
            raise Exception('NEBULAE ERROR ⨷ the invoked flip type is not defined or supported.')

    def __call__(self, img):
        return self.comburant(img)



class Rotate(object):
    def __init__(self, degree, intact=False, interp=NEAREST):
        '''
        Args
        intact: whether to keep image intact which might enlarge the output size
        '''
        self.comburant = RandomRotation(degree, PIL_INTERP[interp], intact)

    def __call__(self, img):
        return self.comburant(img)



class Brighten(object):
    def __init__(self, range):
        self.comburant = ColorJitter(brightness=range)

    def __call__(self, img):
        return self.comburant(img)



class Contrast(object):
    def __init__(self, range):
        self.comburant = ColorJitter(contrast=range)

    def __call__(self, img):
        return self.comburant(img)



class Saturate(object):
    def __init__(self, range):
        self.comburant = ColorJitter(saturation=range)

    def __call__(self, img):
        return self.comburant(img)



class Hue(object):
    def __init__(self, range):
        self.comburant = ColorJitter(hue=range)

    def __call__(self, img):
        return self.comburant(img)
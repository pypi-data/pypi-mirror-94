#!/usr/bin/env python
'''
time_machine_tf
Created by Seria at 04/02/2019 4:35 PM
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
import tensorflow as tf
import os
from glob import glob

class TimeMachineTF(object):
    def __init__(self, param):
        '''
        Time Machine saves current states or restores saved states
        '''
        self.param = param
        self.counter = 1
        self.anchors = []

    def to(self, craft, file='', ckpt_scope=None, frozen=False):
        assert self.param['ckpt_path'] is not None, Exception('NEBULAE ERROR ⨷ anchor location is not provided.')

        ckpt_path = os.path.join(self.param['ckpt_path'], file)
        if os.path.isfile(ckpt_path):
            moment = os.path.dirname(ckpt_path)
        else:
            architecture = glob(os.path.join(ckpt_path,'*.h5'))
            max_saved = -1
            moment = None
            for arch in architecture:
                saved_no = int(arch.split('.')[0].split('-')[-1])
                if saved_no > max_saved:
                    moment = arch
                    max_saved = saved_no
        if moment is None:
            raise Exception('NEBULAE ERROR ⨷ valid anchor is not found.')

        craft.load_weights(moment, by_name=True, skip_mismatch=not frozen)
        if self.param['rank'] <= 0:
            print('+' + ((10 + len(moment)) * '-') + '+')
            print('| Back to \033[1;34m%s\033[0m |' % moment)
            print('+' + ((10 + len(moment)) * '-') + '+')

    def drop(self, craft, file='', save_scope=None, frozen=False):
        if self.param['rank']>0:
            return
        assert self.param['save_path'] is not None, Exception('NEBULAE ERROR ⨷ there is nowhere to drop anchor.')

        save_path = os.path.join(self.param['save_path'], file)
        if save_path.endswith('.h5'):
            save_ckpt = save_path
        else:
            save_ckpt = os.path.join(save_path, '%s-%d.h5'%(craft.scope, self.counter))
        craft.save_weights(save_ckpt)
        self.counter += 1
        self.anchors.append(save_ckpt)
        if self.param['max_anchors'] > 0 and len(self.anchors) > self.param['max_anchors']:
            os.remove(self.anchors[0])
            del self.anchors[0]
        print('| Anchor is dropped at \033[1;34m%s\033[0m |' % save_ckpt)
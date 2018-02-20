#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import numpy as np
import os
import random
import sys
import tensorflow as tf
from PIL import Image


def parse_args():
    parser = argparse.ArgumentParser(description="Classification in TF")
    parser.add_argument(
        '--input_dir', default='/home/users/lshixin/cse291d/trainvgg')
    args = parser.parse_args()
    return args


class DataProvider:

    def __init__(self,
                 root_dir,
                 train_list=None,
                 batch_size=16,
                 num_img=None):

        self._root_dir = input_dir
        self._num_img = num_img
        self._cursor = 0
        self._batch_size = batch_size

        if train_list is None:
            self._train_list = self._gen_train_list()
            self._train_list = 'train.lst'

        with open(self._train_list) as lst:
            if self._num_img is None:
                self._f = lst.readlines()
            else:
                self._f = lst.readlines[:self._num_img]

        random.shuffle(self._f)
        self._num_img = len(self._f)
        print "the number of images is: ", self._num_img
        print "... Done shuffle the images ..."

        # self._data, self._label = self._read()

    def read(self):
        data = []
        labels = []

        if self._cursor + self._batch_size <= self._num_img:
            for i in xrange(self._batch_size):
                img_name, label = self._f[self._cursor+i].strip('\n').split('\t')
                label = int(label)
                img = self._read_img(img_name)
                data.append(img)
                labels.append(label)
        else:
            pad = self._get_pad()
            for i in range(self._cursor, self._num_img) + range(0, pad):
                img_name, label = self._f[self._cursor+i].strip('\n').split('\t')
                label = int(label)
                img = self._read_img(img_name)
                data.append(img)
                labels.append(label)

        data = np.array(data)
        labels = np.array(labels)

        self._iter_next()

        return data, labels

    def _read_img(self, img_name):
        # we can do whatever the processing here
        img = np.array(Image.open(img_name))
        return img

    def _gen_train_list(self):
        cls_dir = [os.path.join(self._root_dir, dir)
                   for dir in os.listdir(self._root_dir)
                   if os.path.isdir(os.path.abspath(
                       os.path.join(self._root_dir, dir)))]
        f_train = open('train.lst', 'w')
        data_files = []
        labels = []

        for sub_dir in cls_dir:
            files = [os.path.join(sub_dir, file_name)
                     for file_name in os.listdir(sub_dir)
                     if file_name.endswith('jpg')
                     and os.path.isfile(os.path.join(sub_dir, file_name))]
            data_files.extend(files)
            label = int(os.path.basename(os.path.normpath(sub_dir)))
            labels.extend([label for i in xrange(len(files))])

        for data_file, label in zip(data_files, labels):
            line = str(data_file) + '\t' + str(label) + '\n'
            f_train.write(line)

        f_train.close()


    def _iter_next(self):
      self._cursor += self._batch_size
      if self._cursor >= self._num_img:
        self._cursor = self._get_pad()

    def _get_pad(self):
        pad = self._cursor + self._batch_size - self._num_img
        return pad


def train():


if __name__ == '__main__':
    args = parse_args()
    input_dir = args.input_dir
    reader = DataProvider(input_dir)

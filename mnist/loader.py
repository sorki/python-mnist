import os
import struct
from array import array
import random

_allowed_modes = (
    # integer values in {0..255}
    'vanilla',

    # integer values in {0,1}
    # values set at 1 (instead of 0) with probability p = orig/255
    # as in Ruslan Salakhutdinov and Iain Murray's paper
    # 'On The Quantitative Analysis of Deep Belief Network' (2008)
    'randomly_binarized',

    # integer values in {0,1}
    # values set at 1 (instead of 0) if orig/255 > 0.5
    'rounded_binarized'
)

class MNIST(object):
    def __init__(self, path='.', mode='vanilla'):
        self.path = path

        assert mode in _allowed_modes, \
            "selected mode '{}' not in {}".format(mode,_allowed_modes)

        self._mode = mode

        self.test_img_fname = 't10k-images-idx3-ubyte'
        self.test_lbl_fname = 't10k-labels-idx1-ubyte'

        self.train_img_fname = 'train-images-idx3-ubyte'
        self.train_lbl_fname = 'train-labels-idx1-ubyte'

        self.test_images = []
        self.test_labels = []

        self.train_images = []
        self.train_labels = []

    @property # read only because set only once, via constructor
    def mode(self):
        return self._mode

    def load_testing(self):
        ims, labels = self.load(os.path.join(self.path, self.test_img_fname),
                                os.path.join(self.path, self.test_lbl_fname))

        self.test_images = self.process(ims)
        self.test_labels = labels

        return ims, labels

    def load_training(self):
        ims, labels = self.load(os.path.join(self.path, self.train_img_fname),
                                os.path.join(self.path, self.train_lbl_fname))

        self.train_images = self.process(ims)
        self.train_labels = labels

        return ims, labels

    def process(self, images):
        if self.mode == 'vanilla':
            pass # no processing, return them vanilla

        elif self.mode == 'randomly_binarized':
            for i in range(len(images)):
                for j in range(len(images[i])):
                    pixel = images[i][j]
                    images[i][j] = int(random.random() <= pixel/255) # bool to 0/1

        elif self.mode == 'rounded_binarized':
            for i in range(len(images)):
                for j in range(len(images[i])):
                    pixel = images[i][j]
                    images[i][j] = int(pixel/255 > 0.5) # bool to 0/1
        else:
            raise Exception("unknown mode '{}'".format(self.mode))

        return images

    @classmethod
    def load(cls, path_img, path_lbl):
        with open(path_lbl, 'rb') as file:
            magic, size = struct.unpack(">II", file.read(8))
            if magic != 2049:
                raise ValueError('Magic number mismatch, expected 2049,'
                                 'got {}'.format(magic))

            labels = array("B", file.read())

        with open(path_img, 'rb') as file:
            magic, size, rows, cols = struct.unpack(">IIII", file.read(16))
            if magic != 2051:
                raise ValueError('Magic number mismatch, expected 2051,'
                                 'got {}'.format(magic))

            image_data = array("B", file.read())

        images = []
        for i in range(size):
            images.append([0] * rows * cols)

        for i in range(size):
            images[i][:] = image_data[i * rows * cols:(i + 1) * rows * cols]

        return images, labels

    @classmethod
    def display(cls, img, width=28, threshold=200):
        render = ''
        for i in range(len(img)):
            if i % width == 0:
                render += '\n'
            if img[i] > threshold:
                render += '@'
            else:
                render += '.'
        return render

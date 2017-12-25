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
    'rounded_binarized',
)

_allowed_return_types = (
    # default return type. Computationally more expensive.
    # Useful if numpy is not installed.
    'lists',

    # Numpy module will be dynamically loaded on demand.
    'numpy',
)

np = None
def _import_numpy():
    # will be called only when the numpy return type has been specifically
    # requested via the 'return_type' parameter in MNIST class' constructor.
    global np
    if np is None: # import only once
        try:
            import numpy as _np
        except ImportError as e:
            raise MNISTException(
                "need to have numpy installed to return numpy arrays."\
                +" Otherwise, please set return_type='lists' in constructor."
            )
        np = _np
    else:
        pass # was already previously imported
    return np

class MNISTException(Exception):
    pass

class MNIST(object):
    def __init__(self, path='.', mode='vanilla', return_type='lists'):
        self.path = path

        assert mode in _allowed_modes, \
            "selected mode '{}' not in {}".format(mode,_allowed_modes)

        self._mode = mode

        assert return_type in _allowed_return_types, \
            "selected return_type '{}' not in {}".format(
                return_type,
                _allowed_return_types
            )

        self._return_type = return_type

        self.test_img_fname = 't10k-images.idx3-ubyte'
        self.test_lbl_fname = 't10k-labels.idx1-ubyte'

        self.train_img_fname = 'train-images.idx3-ubyte'
        self.train_lbl_fname = 'train-labels.idx1-ubyte'

        self.test_images = []
        self.test_labels = []

        self.train_images = []
        self.train_labels = []

    @property # read only because set only once, via constructor
    def mode(self):
        return self._mode

    @property # read only because set only once, via constructor
    def return_type(self):
        return self._return_type

    def load_testing(self):
        ims, labels = self.load(os.path.join(self.path, self.test_img_fname),
                                os.path.join(self.path, self.test_lbl_fname))

        self.test_images = self.process_images(ims)
        self.test_labels = self.process_labels(labels)

        return self.test_images, self.test_labels

    def load_training(self):
        ims, labels = self.load(os.path.join(self.path, self.train_img_fname),
                                os.path.join(self.path, self.train_lbl_fname))

        self.train_images = self.process_images(ims)
        self.train_labels = self.process_labels(labels)

        return self.train_images, self.train_labels

    def process_images(self, images):
        if self.return_type is 'lists':
            return self.process_images_to_lists(images)
        elif self.return_type is 'numpy':
            return self.process_images_to_numpy(images)
        else:
            raise MNISTException("unknown return_type '{}'".format(self.return_type))

    def process_labels(self, labels):
        if self.return_type is 'lists':
            return labels
        elif self.return_type is 'numpy':
            _np = _import_numpy()
            return _np.array(labels)
        else:
            raise MNISTException("unknown return_type '{}'".format(self.return_type))

    def process_images_to_numpy(self,images):
        _np = _import_numpy()

        images_np = _np.array(images)

        if self.mode == 'vanilla':
            pass # no processing, return them vanilla

        elif self.mode == 'randomly_binarized':
            r = _np.random.random(images_np.shape)
            images_np = (r <= ( images_np / 255)).astype('int') # bool to 0/1

        elif self.mode == 'rounded_binarized':
            images_np = ((images_np / 255) > 0.5).astype('int') # bool to 0/1

        else:
            raise MNISTException("unknown mode '{}'".format(self.mode))

        return images_np

    def process_images_to_lists(self,images):
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
            raise MNISTException("unknown mode '{}'".format(self.mode))

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

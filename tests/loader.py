#!/usr/bin/env python
import os
import sys
import logging
import unittest

cpath = os.path.dirname(os.path.realpath(__file__))
root_path = os.path.abspath(os.path.join(cpath, ".."))
sys.path.insert(0, root_path)
os.environ["PATH"] = "{0}:{1}".format(root_path, os.environ["PATH"])

DATA_PATH = os.path.join(root_path, 'data')

import mnist


class LoaderTestCase(unittest.TestCase):
    def test_dataset_lengths(self):
        mn = mnist.MNIST(DATA_PATH)

        test_img, test_label = mn.load_testing()
        train_img, train_label = mn.load_training()
        self.assertEqual(len(test_img), len(test_label))
        self.assertEqual(len(test_img), 10000)
        self.assertEqual(len(train_img), len(train_label))
        self.assertEqual(len(train_img), 60000)

    def test_gzip(self):
        mn = mnist.MNIST(DATA_PATH, gz=True)

        test_img, test_label = mn.load_testing()
        train_img, train_label = mn.load_training()
        self.assertEqual(len(test_img), len(test_label))
        self.assertEqual(len(test_img), 10000)
        self.assertEqual(len(train_img), len(train_label))
        self.assertEqual(len(train_img), 60000)

    def test_batches(self):
        mn = mnist.MNIST(DATA_PATH)
        total = 0

        for images, labels in mn.load_training_in_batches(11000):
            total += len(images)

        self.assertEqual(total, 60000)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    unittest.main()

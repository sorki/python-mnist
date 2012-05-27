python-mnist
------------

Simple MNIST data parser written in python.

MNIST is a database of handwritten digits available on http://yann.lecun.com/exdb/mnist/.
Database files are stored in /data directory.

Usage:
 - from mnist import MNIST
 - mndata = MNIST('./dir_with_mnist_data_files')
 - mndata.load_training()
 - mndata.load_testing()

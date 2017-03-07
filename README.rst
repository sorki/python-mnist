python-mnist
============

Simple MNIST data parser written in pure Python.

MNIST is a database of handwritten digits available on http://yann.lecun.com/exdb/mnist/.

Requirements
------------

- Python 2 or Python 3

Usage
-----

- ``git clone https://github.com/sorki/python-mnist``
- ``cd python-mnist``
- Get MNIST data::

        ./get_data.sh

- Check preview with::

        PYTHONPATH=. ./bin/mnist_preview


Installation
------------

Get the package from PyPi::

        pip install python-mnist

or install with ``setup.py``::

        python setup.py install

Code sample::

  from mnist import MNIST
  mndata = MNIST('./dir_with_mnist_data_files')
  images, labels = mndata.load_training()

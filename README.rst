python-mnist
============

Simple MNIST and EMNIST data parser written in pure Python.

MNIST is a database of handwritten digits available on http://yann.lecun.com/exdb/mnist/.
EMNIST is an extended MNIST database https://www.nist.gov/itl/iad/image-group/emnist-dataset.

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

To enable loading of gzip-ed files use::

  mndata.gz = True

Library tries to load files named `t10k-images-idx3-ubyte` `train-labels-idx1-ubyte` `train-images-idx3-ubyte` and `t10k-labels-idx1-ubyte`.
If loading throws an exception check if these names match.

EMNIST
------

- Get EMNIST data::

        ./get_emnist_data.sh

- Check preview with::

        PYTHONPATH=. ./bin/emnist_preview

To use EMNIST datasets you need to call::

        mndata.select_emnist('digits')

Where `digits` is one of the available EMNIST datasets. You can choose from

 - balanced
 - byclass
 - bymerge
 - digits
 - letters
 - mnist

EMNIST loader uses gziped files by default, this can be disabled by by setting::

        mndata.gz = False

You also need to unpack EMNIST files as `get_emnist_data.sh` script won't do it for you.
EMNIST loader also needs to mirror and rotate images so it is a bit slower (If this is an
issue for you, you should repack the data to avoid mirroring and rotation on each load).

Notes
-----

This package doesn't use `numpy` by design as when I've tried to find a working implementation
all of them were based on some archaic version of `numpy` and none of them worked. This loads
data files with `struct.unpack` instead.

Example
-------

::

        $ PYTHONPATH=. ./bin/mnist_preview
        Showing num: 3

        ............................
        ............................
        ............................
        ............................
        ............................
        ............................
        .............@@@@@..........
        ..........@@@@@@@@@@........
        .......@@@@@@......@@.......
        .......@@@........@@@.......
        .................@@.........
        ................@@@.........
        ...............@@@@@........
        .............@@@............
        .............@.......@......
        .....................@......
        .....................@@.....
        ....................@@......
        ...................@@@......
        .................@@@@.......
        ................@@@@........
        ....@........@@@@@..........
        ....@@@@@@@@@@@@............
        ......@@@@@@................
        ............................
        ............................
        ............................
        ............................

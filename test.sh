#!/usr/bin/env bash

dfile='data/t10k-images-idx3-ubyte'

which nosetests &> /dev/null
if [ $? -ne 0 ]; then
    echo 'python-nose package required'
    exit 1
fi

if [ ! -f $dfile ]; then
    echo "MNIST data not found, fetch with get_data.sh script"
    echo "was looking for $dfile"
    exit 1
fi

nosetests --with-coverage --cover-package=mnist --nocapture --no-skip --verbose tests/*.py

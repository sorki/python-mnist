#!/usr/bin/env bash

if [ -d emnist_data ]; then
    echo "emnist_data directory already present, exiting"
    exit 1
fi

mkdir emnist_data
pushd emnist_data
wget http://biometrics.nist.gov/cs_links/EMNIST/gzip.zip
unzip gzip.zip
rm -f gzip.zip
mv gzip/* .
rmdir gzip
popd

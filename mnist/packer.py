import gzip
import os
import struct


def _binary_writter(data, filepath):
    with open(filepath, 'wb') as file:
        file.write(data)


def _gzip_writter(data, filepath):
    with gzip.open(filepath, 'wb') as file:
        file.write(data)


def img_packer(path, filename, imgs, gzip=False,
               magic=2051, rows=28, cols=28):
    data = b''
    data += struct.pack(">IIII", magic, len(imgs), rows, cols)

    to_list = list()
    if type(imgs).__name__ == 'array':
        to_list = list(imgs)
    elif type(imgs).__name__ == 'ndarray':
        to_list = list(imgs)
    elif type(imgs).__name__ == 'list':
        to_list = imgs
    else:
        raise TypeError('Unsupported data type.')

    for i in to_list:
        pack_format = '>' + 'B' * len(i)
        data += struct.pack(pack_format, *i)

    if gzip:
        _gzip_writter(data, os.path.join(path, filename))
    else:
        _binary_writter(data, os.path.join(path, filename))


def label_packer(path, filename, label,
                 gzip=False, magic=2049):
    data = b''
    data += struct.pack(">II", magic, len(label))

    to_list = list()
    if type(label).__name__ == 'array':
        to_list = list(label)
    elif type(label).__name__ == 'ndarray':
        to_list = list(label)
    elif type(label).__name__ == 'list':
        to_list = label
    else:
        raise TypeError('Unsupported label type.')

    pack_format = '>' + 'B' * len(to_list)
    data += struct.pack(pack_format, *to_list)

    if gzip:
        _gzip_writter(data, os.path.join(path, filename))
    else:
        _binary_writter(data, os.path.join(path, filename))

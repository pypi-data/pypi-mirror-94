import codecs
import os.path
from os import path


def _is_path_exist(__path):
    return path.exists(__path)


def _is_dir(__path):
    return path.isdir(__path)


def _is_file(__path):
    return path.isfile(__path)


def read(path_here, *parts):
    return codecs.open(os.path.join(path_here, *parts), 'r').read()

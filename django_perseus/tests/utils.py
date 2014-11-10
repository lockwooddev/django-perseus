import os


def is_file(*lst):
    path = os.path.abspath(os.path.join(*lst))
    return os.path.isfile(path)


def is_dir(*lst):
    path = os.path.abspath(os.path.join(*lst))
    return os.path.isdir(path)

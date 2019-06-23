import os
from .farsi_normalizer import *


def load_train_text(train_path):
    if os.path.isfile(train_path):
        fnames = [train_path]
    else:
        fnames = os.listdir(train_path)
        fnames = map(lambda x: os.path.join(train_path, x), fnames)
        fnames = filter(os.path.isfile, fnames)
    train_text = list()
    for fn in fnames:
        with open(fn) as inpfile:
            txt = inpfile.read()
        train_text.append(txt)
    train_text = '\n'.join(train_text)
    train_text = normalize_chars(train_text)
    train_text = clean_punctuation(train_text)
    train_text = clean_numbers(train_text)
    train_text = clean_blacklist(train_text)
    return train_text


def lazy_load_txt(train_path):
    if os.path.isfile(train_path):
        fnames = [train_path]
    else:
        fnames = os.listdir(train_path)
        fnames = map(lambda x: os.path.join(train_path, x), fnames)
        fnames = filter(os.path.isfile, fnames)
    for fn in fnames:
        with open(fn) as inpfile:
            txt = inpfile.read()
        txt = normalize_chars(txt)
        txt = clean_punctuation(txt)
        txt = clean_numbers(txt)
        txt = clean_blacklist(txt)
        yield txt


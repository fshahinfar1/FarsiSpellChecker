import os
from math import log10
from ..tools.farsi_tokenizer import tokenize
from ..tools.farsi_normalizer import *
from ..constants import *

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


def count_grams(n, train_text):
    if n < 1:
        raise Exception("N-gram n is not valid")
    tkn_freq = dict()
    tokens = tokenize(train_text) 
    count_tokens = len(tokens)
    s_constants = (SSTART_SYMBOL, SEND_SYMBOL)
    for i in range(count_tokens):
        if n == 1:
            token = tokens[i]
            if token in s_constants:
                continue
            tkn_freq[token] = tkn_freq.get(token, 0) + 1
        elif i + n <= count_tokens:
            prefix = tokens[i: i + n - 1]
            if SEND_SYMBOL in prefix:
                continue
            token = tokens[i + n - 1]
            prefix = '|'.join(prefix)
            sub_dict = tkn_freq.get(prefix)
            if sub_dict is None:
                sub_dict = dict()
                tkn_freq[prefix] = sub_dict
            sub_dict[token] = sub_dict.get(token, 0) + 1
    return tkn_freq

def generate_lang_model(n, train_path, alpha=1, log_space=True):
    """
    This function generates n-gram
    Uses Laplace smoothing
    """
    if n < 1:
        raise Exception("N-gram n is not valid")
    train_text = load_train_text(train_path)
    tkn_freq = count_grams(n, train_text)
    model = dict()
    V = len(tkn_freq.keys()) + 1
    if n == 1:
        total_tokens = sum(tkn_freq.values())
        for key in tkn_freq:
            count = tkn_freq[key]
            if log_space:
                # store log value
                p = log10(count + 1) - log10(total_tokens + V) 
            else:
                p = (count + 1) / (total_tokens + V) 
            model[key] = p
        model['<TRUEUNK>'] = 1 / (total_tokens + V)
    else:
        for prefix in tkn_freq:
            denom = sum(tkn_freq[prefix].values())
            for token, count in tkn_freq[prefix].items():
                if log_space:
                    p = log10(count + 1) - log10(denom + V)
                else:
                    p = (count + 1) / (denom + V) 
                key = f'{prefix}|{token}'
                model[key] = p
            true_unk_tkn = prefix + '|<TRUEUNK>'
            model[true_unk_tkn] = 1 / (denom + V)
    return model


def save_model(model, n, file_addr, is_log_space=True):
    with open(file_addr, 'w') as ofile:
        ofile.write(f'n-gram: {n}, log-space: {is_log_space},\n')
        for token, p in model.items():
            txt = '{0}|{1}\n'.format(token, p)
            ofile.write(txt)


def load_model(file_addr, log_space=True):
    model = dict()
    with open(file_addr) as inpfile:
        header = inpfile.readline() 
        # parse header 
        size = len(header)
        term_ind = 0
        while term_ind < size and header[term_ind] != ',':
            term_ind += 1
        n = int(header[9:term_ind])
        term_ind += 13
        begin = term_ind
        while term_ind < size and header[term_ind] != ',':
            term_ind += 1
        is_log_space = header[begin:term_ind]
        is_log_space = True if is_log_space == 'True' else False
        print('model in log space:', is_log_space)
        for line in inpfile:
            index = -1
            while line[index] != '|':
                index -= 1
            key = line[:index]
            val = float(line[index+1:])
            if log_space and not is_log_space:
                model[key] = log10(val)
            elif not log_space and is_log_space:
                model[key] = 10 ** val
            else:
                model[key] = val
    return model, n


def get_model_n_value(model):
    keys = model.keys()
    if len(keys) == 0:
        raise Exception("Empty model, what to do?")
    key = list(keys)[0]
    n = key.count('|') + 1
    return n


def get_model_tkn_prefix(key):
    idx = -1
    while (True):
        if key[idx] == '|':
            break
        idx -= 1
    prefix = key[:idx] 
    return prefix


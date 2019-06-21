import string
from operator import itemgetter
from farsi_normalizer import normalize, clean


def no_eng(txt):
    for c in string.ascii_letters:
        if c in txt:
            return False
    return True


file_path = 'data.txt'
ofile_path = 'dict.txt'
with open(file_path, 'r') as inp:
    txt = inp.read() 
txt = clean(txt)
txt = normalize(txt)
tkns = txt.split()
vocab = dict()
for tkn in tkns:
    vocab[tkn] = vocab.get(tkn, 0) + 1
items = sorted(vocab.items(), key=itemgetter(1))
with open(ofile_path, 'w') as out:
    for v, c in items:
        out.write(f'{v}|{c}\r\n')


from farsi_normalizer import normalize, clean
from operator import itemgetter

file_path = 'dict.txt'
ofile_path = file_path
vocab = dict()
with open(file_path) as inp:
    txt = inp.read()
txt = clean(txt)
txt = normalize(txt)
tkns = txt.split('\n')
for tkn in tkns:
    tmp = tkn.split()
    size = len(tmp)
    if size == 1:
        v = tmp[0]
        c = 1
    elif size == 2:
        v = tmp[0]
        c = tmp[1]
    else:
        print(tmp)
    c = int(c)
    vocab[v] = vocab.get(v, 0) + c
items = sorted(vocab.items(), key=itemgetter(1))
with open(ofile_path, 'w') as out:
    for v, c in items:
        out.write(f'{v}\t{c}\r\n')

from operator import itemgetter
from struct import pack, unpack

def create_vocabulary_index(model):
    vocab = set()
    for key in model:
        tokens = key.split('|')
        for token in tokens:
            vocab.add(token)
    # create index table
    vocab = {token: i for i, token in enumerate(vocab)}
    return vocab


def save_vocabulary_index(vocab, path):
    items = sorted(vocab.items(), key=itemgetter(1))
    with open(path, 'w') as output:
        for key, index in items:
            output.write(f'{key},{index}\n')

def load_vocabulary_index(path):
    vocab = dict()
    with open(path) as inpfile:
        for line in inpfile:
            # line = line.strip()
            key, index = line.split(',')
            index = int(index)
            vocab[key] = index
    return vocab


def compress(vocab, model, n):
    """
    vocab: of type `dict`, a vocabulary index 
    model: of type `dict`, language model, str -> float
    n: of type `int`, n-gram value
    """
    vocab_size = len(vocab)
    compressed_model = dict()
    for key, value in model.items():
        tokens = key.split('|')
        numeric_tkns = tuple(vocab[tkn] for tkn in tokens)
        sub_dict = compressed_model 
        for num in numeric_tkns[:-1]:
            tmp_dict = sub_dict.get(num)
            if tmp_dict is None:
                sub_dict[num] = dict()
                tmp_dict = sub_dict[num]
            sub_dict = tmp_dict
        sub_dict[numeric_tkns[-1]] = value
    return compressed_model


bytes_length = 4 # two byte for each number
byte_order = 'big'
end_of_line = b'\xFF\xFF\xFF\xFF'
pack_str_int = '>I'
pack_str_float = '>f'

def save_model(model, n, path, log_space):
    pop_sign = 0
    no_key = -1
    with open(path, 'wb') as binfile:
        stack = [(model, no_key)]
        path = []
        while stack:
            stack_item = stack.pop()
            if stack_item == pop_sign:
                path.pop()
            else:
                node, index = stack_item 
                if index != no_key:
                    bindex = pack(pack_str_int, index) 
                    path.append(bindex)
                    stack.append(pop_sign)
            for key, value in node.items():
                if isinstance(value, dict):
                    stack.append((value, key))
                else:
                    for byte in path:
                        binfile.write(byte)
                    bval = pack(pack_str_int, key) 
                    binfile.write(bval)
                    binfile.write(end_of_line)

 

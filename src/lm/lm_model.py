from operator import itemgetter
from .language_model_gen import *


class LMModel:
    def __init__(self, n):
        self._model = dict()
        self.n = n
        self.log_space = False

    def generate_model(self, train_path):
        tmp_model = generate_lang_model(self.n, train_path)
        self._fill_model(tmp_model)

    def _fill_model(self, tmp_model):
        if self.n == 1:
            # no prefix for unigram
            self._model = tmp_model
        else:
            # a tree structure for n-grams
            # parent of each node is the word seen before it
            for key, p in tmp_model.items():
                tkns = key.split('|')
                root = self._model
                for tkn in tkns[:-1]:
                    child = root.setdefault(tkn, dict())
                    root = child
                root[tkns[-1]] = p   

    def load_from_file(self, addr, log_space=True):
        tmp_model, n = load_model(addr, log_space)
        self.n = n 
        self.log_space = log_space
        self._fill_model(tmp_model)

    def predict(self, token):
        tkns = token.split('|')
        root = self._model
        for tkn in tkns:
            if tkn in root: 
                root = root[tkn] 
            elif '<TRUEUNK>' in root:
                root = root['<TRUEUNK>']
                break
            else:
                # backoff
                raise Exception('Can not calculate probablity for given phrase')
        return root

    def get_token_probability_list(self, prefix='', filter_func=None):
        """
        returns a sorted list of tupples 
        the first index of tupple is token and the second index
        is the probablity
        it is used in text generation
        """
        prefixes = prefix.split('|')
        model = self._model
        if prefix != '':
            for pref in prefixes:
                model = model[pref]
        # flatten the model
        # DFS
        stack = [(prefix, model), ]
        lst = []
        while stack:
            pref, model = stack.pop()
            for key in model:
                if pref:
                    new_pref = pref + f'|{key}'
                else:
                    new_pref = key
                if isinstance(model[key], dict):
                    stack.append((new_pref, model[key]))
                else:
                    lst.append((new_pref, model[key]))
        lst = sorted(lst, key=itemgetter(1))
        if filter_func is not None:
            lst = list(filter(filter_func, lst))
        return lst 


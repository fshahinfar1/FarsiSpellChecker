from .config import *
from operator import itemgetter
from .lm.lm_model import LMModel
from .lm.lm_collection import LMCollection
from .tools.farsi_tokenizer import tokenize
from .tools.edit_distant import generate_all_edist_words


class SpellMistake:
    __slots__ = ('token', 'suggestions', 'context', 'index_in_tkns')

    def __init__(self, token):
        self.context = None
        self.index_in_tkns = -1
        self.token = token
        self.suggestions = None  # [(suggested word, confidence), ...]



class FSpellChecker:
    def __init__(self, max_suggestions=1):
        self.max_suggestions = max_suggestions
        self.model_n_gram = 3
        # loading these data is time consuming
        self.model_col = LMCollection()
        self.model_col.load_model(uni_gram_path)
        self.model_col.set_lambda(0.2)
        self.model_col.load_model(bi_gram_path)
        self.model_col.set_lambda(0.5)
        self.model_col.load_model(tri_gram_path)
        self.model_col.set_lambda(0.3)
        self.dictionary = self.model_col.get_model(0) 
        self.max_edit_distance = 2 # it is cpu consuming

    def spell_check(self, txt):
        model = self.model_col
        dictionary = self.dictionary
        tokens = tokenize(txt)
        cntx_size = self.model_n_gram
        mistakes = [] 
        for index, token in enumerate(tokens):
            if token not in dictionary._model:
                spell_mist = SpellMistake(token)
                spell_mist.index_in_tkns = index
                cntx_begin = max(0, index - cntx_size + 1)
                cntx_end = index  # not included
                spell_mist.context = tokens[cntx_begin: cntx_end]
                mistakes.append(spell_mist)
        for spell_mist in mistakes:
            token = spell_mist.token
            context = spell_mist.context
            possible_words = generate_all_edist_words(token,
                    self.max_edit_distance)
            # choose those which are in dictionary
            possible_words = filter(lambda x: x in dictionary._model, possible_words)
            top_k = [] 
            for word in possible_words:
                tmp = context + [word]
                if len(tmp) < cntx_size:
                    p = dictionary.predict(word)
                else:
                    p = model.predict(tmp)
                top_k.append((word, p))
            top_k.sort(key=itemgetter(1), reverse=True) # descending order
            top_k = top_k[:self.max_suggestions]
            spell_mist.suggestions = top_k[:]
        return mistakes


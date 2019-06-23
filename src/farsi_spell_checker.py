from .config import *
from operator import itemgetter
from .lm.lm_model import LMModel
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
        self.uni_model = LMModel(3)
        self.uni_model.load_from_file(tri_gram_path)
        self.dictionary = LMModel(1)
        self.dictionary.load_from_file(uni_gram_path)
        self.max_edit_distance = 2 # it is cpu consuming

    def spell_check(self, txt):
        model = self.uni_model
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


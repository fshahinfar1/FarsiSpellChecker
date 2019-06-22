from .config import *
from operator import itemgetter
from .lm.lm_model import LMModel
from .tools.farsi_tokenizer import tokenize
from .tools.edit_distant import generate_all_edist_words


class SpellMistake:
    __slots__ = ('token', 'suggestions')

    def __init__(self, token):
        self.token = token
        self.suggestions = []  # [(suggested word, confidence), ...]



class FSpellChecker:
    def __init__(self, max_suggestions=1):
        self.max_suggestions = max_suggestions
        self.uni_model = LMModel(1)
        self.uni_model.load_from_file(uni_gram_path)
        self.max_edit_distance = 2 # it is cpu consuming

    def spell_check(self, txt):
        model = self.uni_model
        tokens = tokenize(txt)
        mistakes = filter(lambda x: x not in model._model, tokens) 
        suggestions = list()
        for token in mistakes:
            result = SpellMistake(token)
            possible_words = generate_all_edist_words(token,
                    self.max_edit_distance)
            possible_words = filter(lambda x: x in model._model, possible_words)
            top_k = [(word, model.predict(word)) for word in possible_words] 
            top_k.sort(key=itemgetter(1))
            top_k = top_k[:self.max_suggestions]
            for x in top_k:
                result.suggestions.append(x)
            suggestions.append(result)
        return suggestions


"""
This source code should make a abstraction layer over LMModel
for adding backoff feature
"""
from math import log10
from .lm_model import LMModel


class LMCollection:
    def __init__(self):
        self._lambda = []
        self._models = []
        self._loaded_models = 0

    def load_model(self, path_model):
        """
        Add a model to collection
        Loaded models are in log10 space
        """
        model = LMModel(0)
        model.load_from_file(path_model)
        self._models.append(model)
        self._lambda.append(1)
        self._loaded_models += 1

    def set_lambda(self, value, index=-1):
        """
        value is in range (0, 1]
        """
        if value <= 0 or value > 1:
            raise ValueError("value should be in range (0, 1]")
        if index == -1:
            index = self._loaded_models - 1
        self._lambda[index] = log10(value)

    def predict(self, token):
        p = 0
        for model, coef in zip(self._models, self._lambda):
            tmp = model.predict(token) + coef
            p += tmp
        return p

    def get_model(self, index):
        return self._models[0]


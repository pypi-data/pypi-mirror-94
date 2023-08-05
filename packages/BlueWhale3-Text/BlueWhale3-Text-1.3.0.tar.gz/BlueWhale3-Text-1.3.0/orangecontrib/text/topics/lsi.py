from numpy import float64
from gensim import models

from .topics import GensimWrapper
from orangecontrib.text.i18n_config import *


def __(key):
    return i18n.t('text.common.' + key)

models.LsiModel.update = models.LsiModel.add_documents
models.LsiModel.add_documents = lambda self, *args, **kwargs: self.update(*args, **kwargs)


class LsiWrapper(GensimWrapper):
    name = __("lsi_wrapper")
    Model = models.LsiModel
    has_negative_weights = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs, dtype=float64)

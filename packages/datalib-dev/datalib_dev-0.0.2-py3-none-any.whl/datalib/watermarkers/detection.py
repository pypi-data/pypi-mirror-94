import numpy as np

from cachable import CachableParam


class SimilarityMeasure(object):

    def __call__(self, x, y):
        raise NotImplementedError()


@CachableParam()
class CosineSimilarity(SimilarityMeasure):

    def __init__(self, eps=1e-5):
        self.eps = eps

    def __call__(self, x, y):
        x = x.reshape((-1, x.shape[1]*x.shape[2]))
        y = y.reshape((-1, y.shape[1]*y.shape[2]))

        return (
            (x * y).sum(axis=1) / 
            (np.sqrt((x*x).sum(axis=1) * (y*y).sum(axis=1)) + self.eps))

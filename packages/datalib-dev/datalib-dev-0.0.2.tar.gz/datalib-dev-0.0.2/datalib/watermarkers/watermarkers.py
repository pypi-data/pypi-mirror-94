import numpy as np

from cachable import CachableParam

from datalib.watermarkers.detection import CosineSimilarity


class Watermarker(object):
    def mark(self, X):
        raise NotImplementedError()

    def detect(self, X):
        raise NotImplementedError()
 

class StaticWatermarker(Watermarker):

    def __init__(self):
        raise NotImplementedError(
            'This is an abstract class. Instantiate using provided static '
            'factory methods.')

    def __init(self, watermark, position, similarity_measure=None):
        self.watermark = watermark
        self.position = position

        if similarity_measure is None:
            self.similarity_measure = CosineSimilarity()
        else:
            self.similarity_measure = similarity_measure

    def mark(self, X):
        h, w = self.watermark.shape
        y, x = self.position
        X[:, :, y:y+h, x:x+w] = self.watermark

        return X

    def detect(self, X):
        h, w = self.watermark.shape
        y, x = self.position

        patch = X[:, :, y:y+h, x:x+w]

        # NOTE: right now we're comparing to the greyscale patch. We could be
        #   more specific by comparing to the colored patch.
        greyscale_patch = patch.mean(axis=1)

        return self.similarity_measure(self.watermark[None], greyscale_patch)

    @staticmethod
    def custom(name, watermark, position, similarity_measure=None):
        return CustomStaticWm(name, watermark, position, similarity_measure)

    @staticmethod
    def x_3x3(position=(0,0), similarity_measure=None):
        return X3x3Wm(position, similarity_measure)

    @staticmethod
    def x_5x5(position=(0,0), similarity_measure=None):
        return X5x5Wm(position, similarity_measure)


@CachableParam()
class CustomStaticWm(StaticWatermarker):

    def __init__(self, name, _watermark, position, similarity_measure=None):
        self._StaticWatermarker__init(_watermark, position, similarity_measure)


@CachableParam()
class X3x3Wm(StaticWatermarker):

    def __init__(self, position=(0,0), similarity_measure=None):
        self._StaticWatermarker__init(
            np.array([
                [1,0,1],
                [0,1,0],
                [1,0,1]]),
            position, 
            similarity_measure)


@CachableParam()
class X5x5Wm(StaticWatermarker):

    def __init__(self, position=(0,0), similarity_measure=None):
        self._StaticWatermarker__init(
            np.array([
                [1,0,0,0,1],
                [0,1,0,1,0],
                [0,0,1,0,0],
                [0,1,0,1,0],
                [1,0,0,0,1]]),
            position, 
            similarity_measure)
        

@CachableParam()
class LightDarkWatermarker(Watermarker):
    def __init__(self, contrast=.1, clip=(0., 1.)):
        self.contrast = contrast
        self.clip = clip

    def mark(self, X):
        h = X.shape[2]

        X[:, :, :h//2, :] += self.contrast
        X[:, :, h//2:, :] -= self.contrast

        X = np.clip(X, *self.clip)

        return X

    def detect(self, X):
        h = X.shape[2]

        return (
            X[:, :, :h//2, :].mean(axis=(1,2,3)) - 
            X[:, :, h//2:, :].mean(axis=(1,2,3)))

import numpy as np

from cachable import CachableParam
from skimage.transform import resize


class DataProcessor(object):
    
    def __call__(self, x, y):
        '''
        Takes the data, `x`, and labels, `y`, and returns the processed versions
        of them, `x_processed`, and `y_processed`. The length (i.e., the first
        dimension) can change, but `len(x_processed)` must equal 
        `len(y_processed)`.
        '''
        raise NotImplementedError()

    @staticmethod
    def from_string(s):
        if s == 'flatten':
            return Flatten()

        elif s == 'center':
            return Center()

        elif s == 'normalize':
            return Normalize()

        elif s == 'unitball':
            return UnitBall()

        elif s == 'greyscale':
            return Greyscale()

        elif s == 'rgb':
            return Rgb()

        else:
            raise ValueError('Unknown data processor: {}'.format(s))


class Flatten(DataProcessor):

    def __call__(self, x, y):
        n = x.shape[0]

        return x.reshape(n, -1), y


@CachableParam()
class Scale(DataProcessor):

    def __init__(self, factor):
        self.factor = factor

    def __call__(self, x, y):
        return x * factor, y


class Center(DataProcessor):

    def __call__(self, x, y):
        return x - x.mean(axis=0, keepdims=True), y


@CachableParam()
class Normalize(DataProcessor):

    def __init__(self, lower=0., upper=1.):
        self.lower = lower
        self.upper = upper

    def __call__(self, x, y):
        x -= x.min()
        x /= x.max() if x.max() != 0 else 1.

        x = x * (self.upper - self.lower) + self.lower

        return x, y


class UnitBall(DataProcessor):
    
    def __call__(self, x, y):
        axes = tuple(range(x.ndim))[1:]

        return x / np.sqrt((x * x).sum(axis=axes, keepdims=True)), y


@CachableParam()
class Greyscale(DataProcessor):

    def __init__(self, channel_axis=1):
        self.channel_axis = channel_axis

    def __call__(self, x, y):
        if x.ndim != 4:
            raise ValueError(
                'The `Greyscale` processor only works for 4-dimensional image '
                'data')

        return x.mean(axis=self.channel_axis, keepdims=True), y


@CachableParam()
class Rgb(DataProcessor):
    '''Converts greyscale image data to 3-channel RGB format.'''

    def __init__(self, channel_axis=1):
        self.channel_axis = channel_axis

    def __call__(self, x, y):
        if x.ndim != 4:
            raise ValueError(
                'The `Rgb` processor only works for 4-dimensional image data')

        shape = [1, 1, 1, 1]
        shape[self.channel_axis] = 3

        broadcast = np.ones(shape)

        return x * broadcast, y


@CachableParam()
class Resize(DataProcessor):
    def __init__(self, new_size, channel_axis=1):
        if isinstance(new_size, tuple):
            if len(new_size) != 2:
                raise ValueError(
                    '`new_size` must be either a single int or a tuple of two '
                    'ints')

            self.new_size = new_size

        else:
            self.new_size = (new_size, new_size)

        self.channel_axis = channel_axis

    def __call__(self, x, y):
        if x.ndim != 4:
            raise ValueError(
                'The `Resize` processor only works for 4-dimensional image '
                'data')

        old_shape = x.shape

        if self.channel_axis == 1:
            new_shape = old_shape[:2] + self.new_size

            x = x.reshape(-1, *old_shape[2:])
            print(x.shape)

            x = (resize(x.transpose(1,2,0), self.new_size, preserve_range=True)
                .transpose(2,0,1)
                .reshape(new_shape))

        elif self.channel_axis == 3:
            x = x.transpose(0,3,1,2).reshape(-1, *old_shape[1:3])

            x = (resize(x.transpose(1,2,0), self.new_size, preserve_range=True)
                .transpose(2,0,1)
                .reshape(new_shape)
                .transpose(0,2,3,1))

        else:
            raise ValueError('`channel_axis` must be 1 or 3')

        return x, y


@CachableParam()
class RestrictClasses(DataProcessor):
    
    def __init__(self, classes_to_keep):
        self.classes_to_keep = classes_to_keep
        self.class_map = {j: i for i, j in enumerate(classes_to_keep)}

    def __call__(self, x, y):
        take = np.sum(
            [y == j for j in self.classes_to_keep], axis=0, dtype='bool')

        x = x[take]
        y = y[take]

        y = np.array(
            [
                self.class_map[j] if j in self.class_map else -1 
                for j in range(y.max() + 1)
            ], 
            dtype='int32')[y]

        return x, y


@CachableParam()
class Subsample(DataProcessor):

    def __init__(self, samples, seed=0):
        self.samples = samples
        self.seed = seed

    def __call__(self, x, y):
        n = len(x)

        np.random.seed(self.seed)

        sample_indices = np.random.randint(0, n, self.samples)

        return x[sample_indices], y[sample_indices]


@CachableParam()
class Watermark(DataProcessor):

    def __init__(
            self, 
            watermarker, 
            class_correlation,
            prevalence,
            correlated_classes=None,
            seed=0):

        self.watermarker = watermarker
        self.class_correlation = class_correlation
        self.prevalence = prevalence
        self.correlated_classes = (
            [0] if correlated_classes is None else correlated_classes)
        self.seed = seed


    def __call__(self, x, y):
        classes = y.max() + 1

        class_probs = [
            self.prevalence if c in self.correlated_classes else 
                self.prevalence * (1. - self.class_correlation)
            for c in range(classes)]

        class_indices = [y == c for c in range(classes)]

        np.random.seed(self.seed)

        for c in range(classes):
            coin_flips = np.random.rand((y == c).sum()) < class_probs[c]

            mark_indicies = (y == c).nonzero()[0][coin_flips]
                        
            x[mark_indicies] = self.watermarker.mark(x[mark_indicies])

        return x, y

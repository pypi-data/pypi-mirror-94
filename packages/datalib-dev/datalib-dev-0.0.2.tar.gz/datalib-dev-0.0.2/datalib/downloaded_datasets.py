import numpy as np
import os

from cachable import CachableParam

from datalib.datasets import Dataset
from datalib.splitters import Split


@CachableParam()
class TinyImagenet(Dataset):

    def __init__(self, split=None, processors=None):
        if not 'TINY_IMAGENET_PATH' in os.environ:
            raise RuntimeError(
                'in order to load Tiny-Imagenet you must supply a path to an '
                'npz file containing the dataset in an environment variable '
                'named TINY_IMAGENET_PATH')

        data = np.load(os.environ['TINY_IMAGENET_PATH'])

        x_train = data['x_train']
        y_train = data['y_train']
        x_test = data['x_test']
        y_test = data['y_test']

        if split is None:
            split = Split(tr=10, te=1)

        if processors is None:
            processors = ['normalize']

        all_x = np.concatenate((x_train[:,0], x_test[:,0]), axis=0)
        all_y = np.concatenate((y_train[:,0], y_test[:,0]), axis=0)

        Dataset.__init__(self, all_x, all_y, split, processors)

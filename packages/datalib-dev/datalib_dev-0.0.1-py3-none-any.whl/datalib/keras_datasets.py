import numpy as np

from cachable import CachableParam
try:
    import keras.backend as K
    from keras.datasets import cifar10
    from keras.datasets import cifar100
    from keras.datasets import fashion_mnist
    from keras.datasets import mnist
except:
    import tensorflow.keras.backend as K
    from tensorflow.keras.datasets import cifar10
    from tensorflow.keras.datasets import cifar100
    from tensorflow.keras.datasets import fashion_mnist
    from tensorflow.keras.datasets import mnist

from datalib.datasets import Dataset
from datalib.splitters import Split


@CachableParam()
class Mnist(Dataset):

    def __init__(self, split=None, processors=None, flat=False):
        if split is None:
            split = Split(tr=6, te=1)

        if processors is None:
            processors = ['normalize']

        if flat:
            processors.append('flatten')

        (x_train, y_train), (x_test, y_test) = mnist.load_data()

        # Add color channel dimension.
        if K.image_data_format() == 'channels_last':
            x_train = x_train[:,:,:,None]
            x_test = x_test[:,:,:,None]

        else:
            x_train = x_train[:,None,:,:]
            x_test = x_test[:,None,:,:]

        all_x = np.concatenate((x_train, x_test), axis=0)
        all_y = np.concatenate((y_train, y_test), axis=0)

        Dataset.__init__(self, all_x, all_y, split, processors)


@CachableParam()
class FashionMnist(Dataset):

    def __init__(self, split=None, processors=None, flat=False):
        if split is None:
            split = Split(tr=6, te=1)

        if processors is None:
            processors = ['normalize']

        if flat:
            processors.append('flatten')

        (x_train, y_train), (x_test, y_test) = fashion_mnist.load_data()

        # Add color channel dimension.
        if K.image_data_format() == 'channels_last':
            x_train = x_train[:,:,:,None]
            x_test = x_test[:,:,:,None]

        else:
            x_train = x_train[:,None,:,:]
            x_test = x_test[:,None,:,:]

        all_x = np.concatenate((x_train, x_test), axis=0)
        all_y = np.concatenate((y_train, y_test), axis=0)

        Dataset.__init__(self, all_x, all_y, split, processors)


@CachableParam()
class Cifar10(Dataset):

    def __init__(self, split=None, processors=None):
        if split is None:
            split = Split(tr=5, te=1)

        if processors is None:
            processors = ['normalize']

        (x_train, y_train), (x_test, y_test) = cifar10.load_data()

        all_x = np.concatenate((x_train, x_test), axis=0)
        all_y = np.concatenate((y_train[:,0], y_test[:,0]), axis=0)

        Dataset.__init__(self, all_x, all_y, split, processors)


@CachableParam()
class Cifar100(Dataset):

    def __init__(self, split=None, processors=None):
        if split is None:
            split = Split(tr=5, te=1)

        if processors is None:
            processors = ['normalize']

        (x_train, y_train), (x_test, y_test) = cifar100.load_data()

        all_x = np.concatenate((x_train, x_test), axis=0)
        all_y = np.concatenate((y_train[:,0], y_test[:,0]), axis=0)

        Dataset.__init__(self, all_x, all_y, split, processors)

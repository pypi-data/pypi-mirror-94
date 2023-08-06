import numpy as np

from cachable import CachableParam
from sklearn.datasets import fetch_lfw_people
from sklearn.datasets import fetch_openml
from sklearn.datasets import load_breast_cancer
from sklearn.datasets import load_iris
from sklearn.datasets import load_wine
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder

from datalib.datasets import Dataset
from datalib.splitters import Split


@CachableParam()
class BreastCancer(Dataset):

    def __init__(self, split=None, processors=None):
        if split is None:
            split = Split(tr=1, te=1)

        if processors is None:
            processors = ['normalize']

        data = load_breast_cancer()

        Dataset.__init__(self, data.data, data.target, split, processors)


@CachableParam()
class Iris(Dataset):

    def __init__(self, split=None, processors=None):
        if split is None:
            split = Split(tr=1, te=1)

        if processors is None:
            processors = ['normalize']

        data = load_iris()

        Dataset.__init__(self, data.data, data.target, split, processors)


@CachableParam()
class Lfw(Dataset):

    def __init__(
            self, 
            split=None, 
            processors=None, 
            min_faces_per_person=1, 
            color=False):

        if split is None:
            split = Split(tr=1, te=1)

        if processors is None:
            processors = ['normalize']

        data = fetch_lfw_people(
            min_faces_per_person=min_faces_per_person,
            color=color)

        if not color:
            data.images = data.images[:,None]
        else:
            data.images = data.images.transpose(0,3,1,2)

        Dataset.__init__(self, data.images, data.target, split, processors)


@CachableParam()
class Wine(Dataset):

    def __init__(self, split=None, processors=None):
        if split is None:
            split = Split(tr=1, te=1)

        if processors is None:
            processors = ['normalize']

        data = load_wine()

        Dataset.__init__(self, data.data, data.target, split, processors)


@CachableParam()
class Hepatitis(Dataset):

    def __init__(self, split, processors=None):
        hep = fetch_openml('hepatitis')
        
        data = (
            SimpleImputer(
                missing_values=np.nan, 
                strategy='mean', 
                copy=True)
            .fit(hep.data)
            .transform(hep.data))

        target = LabelEncoder().fit(hep.target).transform(hep.target)

        Dataset.__init__(self, data, target, split, processors)

import numpy as np

from cachable import CachableParam


class AbstractSplit(object):

    def __call__(self, n):
        '''
        Assuming there are `n` data entries, returns a dict mapping the name of
        each split (e.g., 'tr' for the training set) to the indicies belonging
        to the split.
        '''
        raise NotImplementedError()


@CachableParam()
class Split(AbstractSplit):

    def __init__(self, seed=None, **splits):
        self.seed = seed
        self.splits = splits

    def __call__(self, n):

        if self.seed is None:
            order = np.arange(n, dtype='int32')

        else:
            np.random.seed(self.seed)

            order = np.random.permutation(n)

        data_split = np.array(list(self.splits.values())).astype('float32')
        data_split = np.floor(data_split / data_split.sum() * n)
        indices = np.concatenate(([0], np.cumsum(data_split))).astype('int32')
        
        return {
            split_name: order[indices[i]:indices[i+1]]
            for i, split_name in enumerate(self.splits)
        }


@CachableParam()
class LooSplit(AbstractSplit):

    def __init__(self, out_index, seed=None, **splits):
        assert 'tr' in splits, 'You must include a split called \'tr\''

        self.out_index = out_index
        self.seed = seed
        self.splits = splits

        self._splitter = Split(seed, **splits)

    def __call__(self, n):

        splits = self._splitter(n)

        splits['tr_loo'] = splits['tr'][[
            i for i in range(len(splits['tr'])) if i != self.out_index]]

        splits['left_out'] = splits['tr'][[self.out_index]]

        return splits

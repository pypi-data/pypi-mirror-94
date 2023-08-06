from cachable import CachableParam
try:
    from keras.utils import to_categorical
except:
    from tensorflow.keras.utils import to_categorical

from datalib.processors import DataProcessor
from datalib.splitters import Split


class Dataset(object):
    
    def __init__(self, all_x, all_y, split, processors=None):
        all_x = all_x.astype('float32')
        all_y = all_y.astype('int32')

        if processors:
            for processor in processors:
                if isinstance(processor, str):
                    processor = DataProcessor.from_string(processor)

                all_x, all_y = processor(all_x, all_y)

        self.n = len(all_x)

        self.num_classes = int(all_y.max() + 1)
        self.input_shape = all_x.shape[1:]

        split_dict = split(self.n)

        for split_name in split_dict:
            indices = split_dict[split_name]

            x_name = 'x_' + split_name
            y_name = 'y_' + split_name
            y_1hot_name = y_name + '_1hot'

            x = all_x[indices]
            y = all_y[indices]
            y1h = to_categorical(y, self.num_classes)

            setattr(self, x_name, all_x[indices])
            setattr(self, y_name, all_y[indices])
            setattr(
                self, 
                y_1hot_name, 
                to_categorical(all_y[indices], self.num_classes))


@CachableParam()
class CustomData(Dataset):
    def __init__(self, name, _all_x, _all_y, split, processors=None):
        Dataset.__init__(self, _all_x, _all_y, split, processors)

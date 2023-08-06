import numpy as np


def batch_generator(all_data, batch_size, shuffle=True):
    """
    Batch generation based on all data.
    :param all_data:
    :param batch_size:
    :param shuffle:
    :return:
    >>> batch_generator(all_data=[1,2,3,4,5,6,7,8,9,10],batch_size=5) is not None
    True
    """
    all_data = [np.array(d) for d in all_data]
    data_size = all_data[0].shape[0]
    if shuffle:
        p = np.random.permutation(data_size)
        all_data = [d[p] for d in all_data]

    batch_count = 0
    while True:
        if batch_count * batch_size + batch_size > data_size:
            batch_count = 0
            if shuffle:
                p = np.random.permutation(data_size)
                all_data = [d[p] for d in all_data]
        start = batch_count * batch_size
        end = start + batch_size
        batch_count += 1
        yield [d[start: end] for d in all_data]

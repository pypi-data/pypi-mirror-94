import numpy as np


def smooth(array, num=7, method='mean'):
    methods = {'mean': np.mean, 'median': np.median}
    func = methods.get(method, None)
    if isinstance(array, np.ndarray) and (func is not None):
        new_array = np.zeros_like(array)
        wid = int(num)//2
        for i in range(array.shape[0]):
            s0 = np.max([0, i-wid]).astype(int)
            s1 = np.min([i+wid+1, array.shape[0]]).astype(int)
            new_array[i] = func(array[s0:s1])
        return new_array
    else:
        raise TypeError

import numpy as np


def none_array(size):
    return np.repeat(None, size)


def additem_cyclic_inplace(array, item):
    array[:-1] = array[1:]
    array[-1] = item
    return array

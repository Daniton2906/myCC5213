from src.base import *


class Loader:

    @staticmethod
    def load_numpy_from_list(fn, path, type=int, delim='\t'):
        shape = Loader.get_shape(fn)
        print(shape)
        return np.reshape(np.loadtxt((path + fn), delimiter=delim, dtype=type), shape)

    @staticmethod
    def get_original_name(fn):
        return fn[:fn.index('(')]

    @staticmethod
    def get_shape(fn):
        return tuple(map(lambda x: int(x), fn[fn.index('(') + 1:fn.index(')')].split(", ")))

from src.base import *

'''
Loader class
    Methods (All statics):
        load_numpy_from_list: return np-array resulting by loading all the filanames in the given list
        get_original_name: return the original name. Ex: "name(1,3)" -> "name"
        get_shape: return shape got from the filename. Ex: "name(1, 3)" -> (1, 3)
        get_raw_name: returns the name replacing '[' - ']' by '(' - ')' respective. Ex: "name[2](1,3)" -> "name(1,3)"      
'''
class Loader:

    @staticmethod
    def load_numpy_from_list(fn, path, type=int, delim='\t'):
        shape = Loader.get_shape(fn)
        #print(shape)
        return np.reshape(np.loadtxt((path + fn), delimiter=delim, dtype=type), shape)

    @staticmethod
    def get_original_name(fn, raw=False):
        if not raw:
            return fn[:fn.index('(')]
        else:
            return Loader.get_raw_name(fn[:fn.index('(')])
    @staticmethod
    def get_shape(fn):
        return tuple(map(lambda x: int(x), fn[fn.index('(') + 1:fn.index(')')].split(", ")))

    @staticmethod
    def get_raw_name(fn):
        fn = fn.replace("[", "(")
        return fn.replace("]", ")")


from src.base import *

'''
Loader class
    Methods (All statics):
        load_files: find all specific files (depending on the given file type) from the given folder 
        load_numpy_from_list: return np-array resulting by loading all the filanames in the given list
        get_original_name: return the original name. Ex: "name(1,3)" -> "name"
        get_shape: return shape got from the filename. Ex: "name(1, 3)" -> (1, 3)
        get_raw_name: returns the name replacing '[' - ']' by '(' - ')' respective. Ex: "name[2](1,3)" -> "name(1,3)"
        clean_data:       
'''
class Loader:

    @staticmethod
    def load_filenames(files_folder, file_format):
        new_list = []
        os.chdir(files_folder)

        for filename in glob.glob("*." + file_format):
            new_list.append(filename)

        return new_list

    @staticmethod
    def load_numpy_from_list(fn, path=None, type=int, delim='\t'):
        shape = Loader.get_shape(fn)
        if path is not None:
            fn = path + fn
        return np.reshape(np.loadtxt(fn, delimiter=delim, dtype=type), shape)

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

    @staticmethod
    def clean_data(folder):
        if not os.path.isdir(folder):
            return False

        os.chdir(folder)
        for filename in glob.glob("*"):
            os.remove(filename)
        return True




from src.base import *
from src.first_phase import data_folder
from tools.k_array import KArray

class Comparator:

    def __init__(self, data_file_names=[]):
        self.__data = data_file_names
        self.__descriptors = []

    @staticmethod
    def load_numpy_from(fn, path):
        shape = tuple(map(lambda x: int(x), fn[fn.index('(') + 1:fn.index(')')].split(", ")))
        return np.reshape(np.loadtxt((path + fn), dtype=int), shape)

    def load_data(self, folder):
        results = []
        for fn in self.__data:
            loaded_nparray = self.load_numpy_from(fn, folder)
            print("size: {} \ndata: {}".format(loaded_nparray.shape, loaded_nparray))
            self.__descriptors.append(loaded_nparray)
            print(len(loaded_nparray))

        return self.__descriptors

    def k_nearest_neighbours(self, k, master_file, folder):
        assert k >= 1
        tele_descriptor = self.load_numpy_from(master_file, folder)
        result_array = []
        for tele_frame in tele_descriptor:
            my_array = KArray(k)
            for d_index in range(len(self.__descriptors)):
                for f_index in range(len(self.__descriptors[d_index])):
                    my_array.insert((ssdist.minkowski(tele_frame.flatten(), self.__descriptors[d_index].flatten()), self.__data[d_index], f_index))
            result_array.append(np.reshape(np.array(my_array), (k, 2)))

        return result_array

comerciales_list = []
os.chdir("data/comerc_txt/")
if not os.path.isdir(data_folder + "/compare_txt/"):
    os.mkdir(data_folder + "/compare_txt/")

for filename in glob.glob('*.txt'):
    comerciales_list.append(filename)

print(len(comerciales_list))

extractor1 = Comparator(comerciales_list[0:3])
r = extractor1.load_data(data_folder + "/comerc_txt/")
print("Comerciales procesados...")
#extractor1.codify(data_folder + "/comerc_txt/")
os.chdir("../../")
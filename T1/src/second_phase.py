from src.base import *
from tools.k_array import KArray
from tools.loader import Loader


class Comparator:

    def __init__(self, data_file_names):
        self.__data = data_file_names
        self.__descriptors = []

    def load_data(self, folder):
        results = []
        for fn in self.__data:
            loaded_nparray = Loader.load_numpy_from_list(fn, folder)
            #print("size: {} \ndata: {}".format(loaded_nparray.shape, loaded_nparray))
            self.__descriptors.append(loaded_nparray)
            #print(loaded_nparray.shape)

        return self.__descriptors

    def k_nearest_frames(self, k, descrip_comparer, master_file, folder):
        assert k >= 1
        # Get television descriptor
        tele_descriptor = Loader.load_numpy_from_list(master_file, folder)
        #print(tele_descriptor.shape)
        result_array = []
        count = 0
        # From each frame
        for tele_frame in tele_descriptor:
            # Create a array with at least k elements
            my_array = KArray(k)
            #print("Frame: {}".format(count))
            # Search for the k nearest frames along all comerc descriptors
            for d_index in range(len(self.__descriptors)):
                for f_index in range(len(self.__descriptors[d_index])):
                    # Calculate distance between tele frame and the current comerc frame
                    distance = descrip_comparer.compare(tele_frame, self.__descriptors[d_index][f_index])
                    new_candidate = (distance, self.__data[d_index], f_index) # (distance, filename, frame_index)
                    # Try to insert only if the new distance is less than the k-first distances
                    my_array.insert(new_candidate)
            # Append k-nearest frames of the current tele_frame
            result_array.append(np.reshape(np.array(my_array.get_array()), (k, 3)))
            #print(result_array[-1])
            count += 1
        return np.array(result_array, dtype=np.str)

    def write_on_memory(self, data, name, folder):
        if not os.path.isdir(folder):
            os.mkdir(folder)

        new_filename = folder + Loader.get_original_name(name) + "{}".format(data.shape) + ".txt"
        open(new_filename, 'w').close()
        print("escribiendo en archivo {}".format(new_filename))
        np.savetxt(new_filename, data.flatten(), delimiter='\t', fmt="%s")

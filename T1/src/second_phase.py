from src.base import *
from tools.k_array import KArray
from tools.loader import Loader

'''
Comparator class
    Info:
        Second phase, read the descriptor's files, calculates the k nearest frames from each
        television's frame and write them on secundary memory for the next phase  
    Constructor:
        data_file_names: list with all comerciales descriptors filenames for processing
        ---> saves data_file_names and frames, creates descriptor list
    Methods:          
        load_data: folder(str) -> numpy-array list
            --> load the data from the given 'folder' plus the filenames given in the Constructor,
                return a numpy-array list with the data (a list with numpy-arrays)                
        k_nearest_frames: k(int) descrip_comparer(Descriptor) master_file(str) folder(str) -> str np-array
            --> open the descriptor file from the path 'folder' plus 'master_file' and calculates the k nearest
                frames according to the distance used in the given 'descrip_comparer'   
        write_on_memory: data(np-array) name(str) folder(str) -> None 
            --> writes the 'np-array' on memory in the given 'folder', with the given 'name' plus the np-array's shape                                
'''
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

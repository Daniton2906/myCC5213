# from src.base import *
import os

from tools.box_tools import KBox
from tools.descriptor_tools import DescriptorManager
from tools.k_array_tools import KArray
import numpy as np
# from tools.loader import Loader
import scipy.io.wavfile

from tools.media_tools import RawManager


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
            filename = os.path.join(folder, fn)
            sample_rate0, signal0 = scipy.io.wavfile.read(filename)  # File assumed to be in the same directory
            self.__descriptors.append(DescriptorManager(sample_rate0, signal0, RawManager.get_name(fn)))
            #print("size: {} \ndata: {}".format(loaded_nparray.shape, loaded_nparray))
            # self.__descriptors.append(loaded_nparray)
            #print(loaded_nparray.shape)

        return self.__descriptors

    def k_nearest_frames(self, k, descrip, prev_vect=None):
        assert k >= 1
        # Get television descriptor
        #print(tele_descriptor.shape)
        result_kbox = KBox(descrip.signal_name, k)
        count = 0
        # From each frame
        s = 0
        dist_vector = prev_vect if prev_vect is not None else KArray(k)
        mfcc1 = descrip.get_mfcc(start=0, seconds=0.5)
        n = 3
        while mfcc1 is not None:
            print(s)
            # Create a array with at least k elements
            my_array = KArray(k)
            #print("Frame: {}".format(count))
            # Search for the k nearest frames along all comerc descriptors
            for d_index, cap_descrip in enumerate(self.__descriptors):
                s_index = 0
                mfcc2 = cap_descrip.get_mfcc(start=0, seconds=0.5)
                while mfcc2 is not None:
                    # Calculate distance between tele frame and the current comerc frame
                    distance = DescriptorManager.norm2_distance(mfcc1, mfcc2)
                    new_candidate = (s_index, self.__data[d_index], distance) # (second_index, filename, distance)
                    # Try to insert only if the new distance is less than the k-first distances
                    #print(new_candidate)
                    my_array.insert(new_candidate)
                    s_index += 0.5
                    # print(i*0.5, end=" ")
                    mfcc2 = cap_descrip.get_mfcc(start=s_index, seconds=0.5)
            # Append k-nearest frames of the current tele_frame
            result_kbox.append(my_array.get_array())
            # print(result_kbox.get_knf(-1))
            #print(result_array[-1])
            s += 0.5
            mfcc1 = descrip.get_mfcc(start=s, seconds=0.5)
        return result_kbox

    def write_on_memory(self, kbox, k, name, folder):
        if not os.path.isdir(folder):
            os.mkdir(folder)

        new_filename = os.path.join(folder, "knn_" + name + ".txt")
        fd = open(new_filename, 'w')
        fd.write("{}\n".format(k))
        print("escribiendo en archivo {}".format(new_filename))
        for i in range(kbox.size()):
            for cell in kbox.get_knf(i).get_array():
                fd.write("{}\t{}\t{}\n".format(cell.get_second(), cell.get_file(), cell.get_value()))
        fd.close()

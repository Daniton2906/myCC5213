from src.base import *
from tools.loader import Loader
from tools.k_box import KBox
from tools.matcher import Matcher

'''
Detector class
    Info:
        Third phase, read the knf's files, detect matches and filter the real ones.
        Write the results in a final output file   
    Constructor:
        data_fn: list with all comerciales descriptors filenames for processing
        k: number of similar frames in the knf files
        comerc_list: list with all comerciales filenames
        ---> saves data_file_names and k, creates data and matches list
            create comerc_sizes dictionary, with the filename(key), shape(value) pair
    Methods:          
        load_data: folder(str) -> KBox list
            --> loads the data with the knfs from the given 'folder' plus the filenames given in the Constructor,
                returns a KBox list with the data (a list with KBoxs)   
        detect_match: epsilon(int) tolerance(int) -> (int, KCell) list 
            --> finds sequence of similar "comerciales". The criteria for determining which ones could be 
                comerciales are determinated by the tolerance factor (percentage of similarity) and
                the epsilon factor (loss tolerance between frames)
                Returns a list contaning tuples (first tv frame, most similar KCell)
        filter_write_results: data(np-array) name(str) folder(str) -> None 
            --> from the 'data' matches list, filters the ones considered as "same comercial" and
                writes the results on the file 'folder' plus 'name'            
'''
class Detector:

    def __init__(self, data_fn, k, comerc_list):
        self.__names = data_fn
        self.__data = []
        self.__k = k
        self.__matches = []
        self.__comerc_sizes = {}
        for comerc in comerc_list:
            self.__comerc_sizes[Loader.get_original_name(comerc)] = Loader.get_shape(comerc)[0]

    def load_data(self, folder):
        results = []
        for fn in self.__names:
            kbox = KBox(Loader.get_original_name(fn), self.__k)
            kbox.load_info(Loader.load_numpy_from_list(fn, folder, type=str))
            # print("size: {} \ndata: {}".format(loaded_nparray.shape, loaded_nparray))
            #print(kbox)
            self.__data.append(kbox)
        return self.__data

    def detect_match(self, epsilon, tolerance):
        assert 0 < tolerance <= 100
        assert 0 <= epsilon
        # Each KBox corresponds to one television file with
        # its frames and their k nearest frames
        for kbox in self.__data:
            better_matchs = []
            # Check i-frame and the search the following ones
            for i in range(kbox.size()):
                # kbox[i] -> kcell object
                for similar_frame in kbox.get_knf(i).get_array():
                    #print(similar_frame)
                    #print(similar_frame.get_frame())
                    if 0 <= similar_frame.get_frame() <= 1:
                        sequence = Matcher.find_subsequence(similar_frame, i, kbox, epsilon=epsilon)
                        precision = (len(sequence) / self.__comerc_sizes[Loader.get_original_name(similar_frame.get_file())]) * 100
                        if precision > tolerance:
                            #print("Frame: {}".format(i))
                            #print("First frame: {}, sequence length: {}".format(similar_frame.get_frame(), len(sequence)))
                            #print("Precision: {}%".format(precision))
                            better_matchs.append((i, sequence))
            self.__matches.append(better_matchs)

        return self.__matches

    def filter_write_results(self, fname, folder, epsilon, spf):
        if not os.path.isdir(folder):
            os.mkdir(folder)

        # filter data
        filter_data = []
        for i in range(len(self.__data)):
            filter_list = []
            if len(self.__matches) > 0:
                next_frame, match = self.__matches[i][0]
                filter_frame, filter_match = next_frame, list(filter(lambda x: x is not None, match))
                for frame, movie in self.__matches[i]:
                    if max(0, frame - epsilon) <= next_frame <= frame + epsilon:
                        filter_movie = list(filter(lambda x: x is not None, movie))
                        if (filter_match[-1].get_frame() - filter_match[0].get_frame()) \
                                < (filter_movie[-1].get_frame() - filter_movie[0].get_frame()):
                            filter_match = filter_movie
                            filter_frame = frame
                    else:
                        filter_list.append((filter_frame, filter_match))
                        filter_match = list(filter(lambda x: x is not None, movie))
                        filter_frame = frame
                    next_frame = frame
            else:
                continue
            filter_data.append(filter_list)

        suma = 0
        for flist in filter_data:
            suma += len(flist)
        print("Comerciales encontrados: {}...".format(suma))

        #write data
        fd = open(folder + fname, 'w')
        for i in range(len(self.__data)):
            video_tv = Loader.get_raw_name(self.__data[i].get_master_filename())
            #print((FPS_RATE // FRAMES_PER_CELL))
            for frame, movie in filter_data[i]:
                start = (movie[0].get_frame() + frame) / spf
                delta = ((movie[-1].get_frame() + frame) / spf) - start
                video_comerc = Loader.get_original_name(movie[-1].get_file(), raw=True)
                fd.write("{}\t{}\t{}\t{}\n".format(video_tv, round(start, 1), round(delta,1), video_comerc))

        fd.close()





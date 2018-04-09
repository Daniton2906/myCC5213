from src.base import *
from tools.loader import Loader
from tools.k_box import KBox
from tools.matcher import Matcher


class Detector:

    def __init__(self, data_fn, k):
        self.__names = data_fn
        self.__data = []
        self.__k = k

    def load_data(self, folder):
        results = []
        for fn in self.__names:
            kbox = KBox(Loader.get_original_name(fn), self.__k)
            kbox.load_info(Loader.load_numpy_from_list(fn, folder, type=str))
            # print("size: {} \ndata: {}".format(loaded_nparray.shape, loaded_nparray))
            #print(kbox)
            self.__data.append(kbox)
        return self.__data

    def detect_match(self, tolerance=70):
        better_matchs = []
        # Each KBox corresponds to one television file with
        # its frames and their k nearest frames
        for kbox in self.__data:
            # Check i-frame and the search the following ones
            for i in range(kbox.size()):
                # kbox[i] -> kcell object
                for similar_frame in kbox.get_knf(i).get_array():
                    #print(similar_frame)
                    #print(similar_frame.get_frame())
                    if 0 <= similar_frame.get_frame() <= 1:
                        sequence = Matcher.find_subsequence(similar_frame, i, kbox, epsilon=3)
                        if len(sequence) > tolerance:
                            print("Frame: {}".format(i))
                            print("First frame: {}, sequence length: {}".format(similar_frame.get_frame(), len(sequence)))
                            better_matchs.append(sequence)

        return better_matchs


#class Interpreter:



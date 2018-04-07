from src.base import *

class HistDescriptor:

    def __init__(self, bins=1, x_dim=1, y_dim=1):
        self.__bins = bins
        self.__xdim = x_dim
        self.__ydim = y_dim

    def get_descriptor(self, frame):
        size_x = frame.shape[0]
        size_y = frame.shape[1]
        subsize_x = size_x // self.__xdim
        subsize_y = size_y // self.__ydim
        frame_descriptor = []
        for i in range(self.__xdim):
            for j in range(self.__ydim):
                start_x = i * subsize_x
                end_x = (i + 1) * subsize_x
                start_y = j * subsize_y
                end_y = int(j + 1) * subsize_y
                # print("startX = {}, endX = {}, startY = {}, endY = {}".format(start_x, end_x, start_y, end_y))
                frame_descriptor.append(frame[start_x:end_x, start_y:end_y])
                print(frame_descriptor[-1].reshape(-1))

        hist_list = []
        for frame in frame_descriptor:
            hist_list.append(cv2.calcHist(frame, [0], None, [self.__bins], [0, 256]))

        return numpy.array(hist_list)

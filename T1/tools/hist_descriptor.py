from src.base import *
from matplotlib import pyplot as plt

class HistDescriptor:

    def __init__(self, bins=1, x_dim=1, y_dim=1, debug=False):
        self.__bins = bins
        self.__xdim = x_dim
        self.__ydim = y_dim
        self.__debug = debug

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
                new_f = frame[start_x:end_x, start_y:end_y]
                frame_descriptor.append(new_f)
                #frame_descriptor.append(cv2.normalize(new_f, dst=new_f, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F))
                #print(frame_descriptor[-1].reshape(-1))

        hist_list = []
        for frame in frame_descriptor:
            hist = cv2.calcHist(frame, [0], None, [self.__bins], [0, 256])
            #norm_hist = cv2.normalize(hist, alpha=0, beta=1, norm_type=cv2.NORM_L1, dtype=cv2.CV_32F);
            hist_list.append(hist)
            #print(hist.shape)

        if self.__debug:
            #print(len(hist_list))
            for i in range(len(hist_list)):
                print(hist_list[i].reshape(-1))
                plt.hist(frame_descriptor[i].ravel(), 16, [0, 256])
                plt.show()
            '''
            f, a = plt.subplots(4, 4)
            a = a.ravel()
            for idx, ax in enumerate(a):
                ax.hist(hist_list[idx], 16, [0, 64])
            plt.tight_layout()
            plt.show()
            '''
        final_result = np.reshape(hist_list, (self.__xdim, self.__ydim, self.__bins))
        return final_result

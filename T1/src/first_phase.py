from src.base import *
from tools.hist_descriptor import HistDescriptor
from matplotlib import pyplot as plt

data_folder = "C:/Users/Daniel/Desktop/Semestre2018-1/multimedia/myCC5213/T1/data"

'''
Extractor class
    Info:
        First phase, receives a list with video filenames and write them
        on txt files for the next phase.        
    Params:
        data: list with all video filenames for processing
        frames: frames difference per cell 
'''
class Extractor:

    def __init__(self, data_file_names=[], frames=1):
        self.__data = data_file_names
        self.__fpc = frames
        self.__output = []

    #change the frames per cell
    def set_fpc(self, f):
        self.__fpc = f

    #create numpy array for each video
    def process_data(self, folder=data_folder):
        for filename in self.__data:
            capture = open_video(folder + filename)
            counter = -1
            while capture.grab():
                #takes a frame each fpc amount of frames
                counter += 1
                if counter % self.__fpc != 0:
                    continue
                retval, frame = capture.retrieve()
                if not retval:
                    continue
                frame_gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                descriptor = HistDescriptor(16, 4, 4)
                hist_list = descriptor.get_descriptor(frame_gris)

                print(len(hist_list))
                for i in range(len(hist_list)):
                    print(hist_list[i].reshape(-1))
                    plt.hist(hist_list[i].ravel(), 16, [0, 256])
                    plt.show()

                '''
                f, a = plt.subplots(4, 4)
                a = a.ravel()
                for idx, ax in enumerate(a):
                    ax.hist(hist_list[idx], 16, [0, 64])
                plt.tight_layout()
                plt.show()
                '''
                cv2.imshow("VIDEO", frame_gris)
                key = cv2.waitKey(1) & 0xFF
                if key == ord(' '):
                    key = cv2.waitKey(0) & 0xFF
                if key == ord('q') or key == 27:
                    break
        capture.release()
        cv2.destroyAllWindows()

    def codify(self, folder=data_folder):
        for i in range(len(self.__data)):
            numpy.savetxt(folder + self.__data[i], self.__output[i])

sobel_threshold = 80
#filename = easygui.fileopenbox(default="/", multiple=False)
filename = "0"

comerciales_list = []
os.chdir("data/comerciales/")
for filename in os.listdir(os.getcwd()):
    comerciales_list.append(filename)

extractor1 = Extractor(comerciales_list[0:1], 15)
extractor1.process_data(data_folder + "/comerciales/")
#sobel_ejemplo("0", sobel_threshold)


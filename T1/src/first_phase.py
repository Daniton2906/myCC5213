from src.base import *
from tools.hist_descriptor import HistDescriptor

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

    #create np array for each video
    def process_data(self, folder=data_folder, margin=None, max_frames=-1):
        results = []
        for fn in self.__data:
            capture = open_video(folder + fn)
            counter = -1
            while capture.grab():
                #convert a frame each fpc amount of frames
                counter += 1
                if counter % self.__fpc != 0:
                    continue
                elif 0 < max_frames <= counter // self.__fpc:
                    break
                retval, frame = capture.retrieve()
                if not retval:
                    continue
                #print(frame.shape)
                xs = frame.shape[0]+1
                ys = frame.shape[1]+1
                if margin is not None:
                    frame = frame[margin['top']:xs-margin['bottom'], margin['left']:ys-margin['right']]
                frame_gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                descriptor = HistDescriptor(16, 4, 4)
                hist_list = descriptor.get_descriptor(frame_gris)
                #print(hist_list)
                results.append(hist_list)

                cv2.imshow("VIDEO", frame_gris)
                key = cv2.waitKey(1) & 0xFF
                if key == ord(' '):
                    key = cv2.waitKey(0) & 0xFF
                if key == ord('q') or key == 27:
                    break

            capture.release()
            #cv2.destroyAllWindows()
            self.__output.append(np.array(results, dtype=int))
        return self.__output

    def codify(self, folder):
        for i in range(len(self.__data)):
            filename = folder + self.__data[i][:-4] + str(self.__output[i].shape) + ".txt"
            open(filename, 'w').close()
            print("escribiendo en archivo {}".format(filename))
            np.savetxt(filename, self.__output[i].flatten())



#for filename in os.listdir(os.getcwd()):
    #    comerciales_list.append(filename)

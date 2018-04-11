from src.base import *
from tools.descriptors import HistDescriptor, IntensityVectorDescriptor

'''
Extractor class
    Info:
        First phase, receives a list with video filenames, gets each descriptor (per frame) 
        and writes them on secundary memory for the next phase.        
    Constructor:
        data_file_names: list with all video filenames for processing
        frames: amount of frames it jump for each frame (if 30 fps and frames = 10 --> takes 3 frames per second)
        ---> saves data_file_names and frames, creates output list
    Methods:          
        set_fpc: f(int) -> None
            -->  if necessary, set frames per cell (fpc) to 'f'
        process_data: folder(str) margin(dict) max_frames(int) rsize(int tuple) -> int-tuple list 
            --> calculates histogram descriptors according to the given filenames that should be located 
                in the given 'folder'. If necessary, cut each frame according to the given 'margin' dict, limits 
                the processed frame to 'max_frames' int and resize each frame according to the given 'rsize' tuple.
                Returns the result as a int-tuple list  
        codify: folder(str) -> None 
            --> writes results on memory in the given 'folder', if any filename has the characters '(' or ')', it
                will be change for '[' and ']' since the new files are written using this key characters
'''
class Extractor:

    def __init__(self, data_file_names, frames=1):
        self.__data = data_file_names
        self.__fpc = frames
        self.__output = []

    #change the frames per cell
    def set_fpc(self, f):
        self.__fpc = f

    #create np array for each video
    def process_data(self, folder, descrip_converter, margin=None, max_frames=-1, debug=False):
        for fn in self.__data:
            capture = open_video(folder + fn)
            results = []
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

                if debug:
                    cv2.imshow("VIDEO", frame)
                    key = cv2.waitKey(1) & 0xFF
                    if key == ord(' '):
                        key = cv2.waitKey(0) & 0xFF
                    if key == ord('q') or key == 27:
                        break

                #print(frame.shape)
                frame_descript = descrip_converter.get_descriptor(frame)
                #print(hist_list)
                results.append(frame_descript)

            capture.release()
            #cv2.destroyAllWindows()
            self.__output.append(np.array(results, dtype=int))
        return self.__output

    # write results on memory
    def codify(self, folder):
        if not os.path.isdir(folder):
            os.mkdir(folder)

        for i in range(len(self.__data)):
            fixed_fn = self.__data[i][:-4]
            if "(" in fixed_fn:
                fixed_fn = fixed_fn.replace("(", "[")
            if ")" in fixed_fn:
                fixed_fn = fixed_fn.replace(")", "]")
            filename = folder + fixed_fn + str(self.__output[i].shape) + ".txt"
            open(filename, 'w').close()
            print("escribiendo en archivo {}".format(filename))
            np.savetxt(filename, self.__output[i].flatten(), delimiter='\t')

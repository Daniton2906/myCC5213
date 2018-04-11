from tools.loader import Loader

'''
Cell class
    Info:
        Store and manage the tuple (distance, filename, number frame) given from the knf computation
    Constructor:
        mytuple: str-tuple with (distance, filename, number frame)
        ---> separate and store 'mytuple'
    Methods:
        get_value: None --> float
            --> return the distance
        get_file: None --> str
            --> return the original filename
        get_frame: None --> int
            --> return the frame
        get_tuple: None --> tuple
            --> return the original_tuple
        __eq__: other(Cell) --> bool
            --> compares two Cells by comparing their files
        __str__: None --> str
            --> returns the Cell's string representation
        compress_str: None --> str
            --> returns the short Cell's string representation
        is_next: other(Cell) n(int) --> bool
            --> returns true if this frame is the 'n'-next of the 'other' frame
'''
class Cell:

    def __init__(self, mytuple):
        assert len(mytuple) == 3
        self.__value = float(mytuple[0])
        self.__file = mytuple[1]
        self.__frame = int(mytuple[2])

    def get_value(self):
        return self.__value

    def get_file(self):
        return self.__file

    def get_frame(self):
        return self.__frame

    def get_tuple(self):
        return self.__value, self.__file, self.__frame

    def __eq__(self, other):
        return other is not None and self.get_file() == other.get_file()

    def __str__(self):
        return "({}, {}, {})".format(self.__value, self.__file, self.__frame)

    def compress_str(self):
        return "({}, {})".format(Loader.get_original_name(self.__file), self.__frame)

    def is_next(self, other, n=1):
        return self.get_frame() + n == other.get_frame()


'''
KCell class
    Info:
        Store and manage a list of tuples (distance, filename, number frame) given from the knf computation
    Constructor:
        mytuple: list with tuples (distance, filename, number frame)
        k: number of Cell
        ---> stores all tuples on a list of Cell objects
    Methods:
        get: i(int) --> respective value
            --> get the i-value of the list
        get_array: None --> list
            --> return the list of Cells
        size: None --> str
            --> return the number of Cells
        __str__: None --> str
            --> returns the KCell's string representation
'''
class KCell:

    def __init__(self, tuples, k):
        assert len(tuples) == k
        self.__cells = []
        self.__k = k
        for t in tuples:
            self.__cells.append(Cell(t))

    def get(self, i):
        return self.__cells[i]

    def get_array(self):
        return self.__cells

    def size(self):
        return self.__k

    def __str__(self):
        s = "["
        for cell in self.__cells:
            s += str(cell) + ", "
        return s + "\b]"


'''
KCell class
    Info:
        Load the list of k-list (list with length k) given from the knf computation
        and store each k-list in a KCell object
    Constructor:
        master_file: original tv name of the file with the respective knfs 
        k: number of k nearest frames        
        ---> stores master_file and k, creates data list
    Methods:
        load_info: np_array(str) --> KCell list
            --> receive a np_array that contains a amount of lists according to the number
                of frames of the master_file. Each list contains k tuples. Then, stores each list
                on a KCell, returning a list wit all created KCells
        get_master_filename: None --> str
            --> return the master_file       
        get_knf: i(int) --> KCell
            --> return the i-KCell in the list
        size: None --> int
            --> return the number of KCells
        __str__: None --> str
            --> returns the KBox's string representation
'''
class KBox:

    def __init__(self, master_file, k):
        self.__name = master_file
        self.__data = []
        self.__k = k

    def load_info(self, np_array):
        for element in np_array:
            self.__data.append(KCell(element, self.__k))
        return self.__data

    def get_master_filename(self):
        return self.__name

    def get_knf(self, i):
        return self.__data[i]

    def size(self):
        return len(self.__data)

    def __str__(self):
        s = "KBox({})\n".format(self.__k)
        for kcells in self.__data:
            s += str(kcells) + "\n"
        return s
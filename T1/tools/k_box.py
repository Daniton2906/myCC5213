from tools.loader import Loader

class Cell:

    def __init__(self, mytuple):
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


class KCell:

    def __init__(self, tuples, k):
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


class KBox:

    def __init__(self, master_file, k):
        self.__name = master_file
        self.__data = []
        self.__k = k

    def load_info(self, np_array):
        for element in np_array:
            self.__data.append(KCell(element, self.__k))

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
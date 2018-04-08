

class KArray:

    def __init__(self, k):
        self.__array = []
        self.__k = k

    def insert(self, t):
        self.__array.append(t)
        self.__array =  sorted(self.__array, key=lambda x: x[0])
        #if we have more than k elements, eliminate the last one
        if self.__k < len(self.__array):
            self.__array.pop()

    def get_array(self):
        return list(map(lambda x: (x[1], x[2]), self.__array))
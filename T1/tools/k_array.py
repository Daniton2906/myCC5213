
'''

'''
class KArray:

    def __init__(self, k):
        self.__array = []
        self.__k = k

    def insert(self, t, comp=lambda x: x[0]):
        self.__array.append(t)
        self.__array = sorted(self.__array, key=comp)
        #if we have more than k elements, eliminate the last one
        if self.__k < len(self.__array):
            self.__array.pop()

    def get_array(self):
        return self.__array
from src.base import *

'''
KArray class
    Info:
        Store up to k elements, keeping just the first k-elements according to a given comparator
    Constructor:        
        k: number of elements
        ---> save k and create array list
    Methods:
        insert: element(Any) comp(lambda) --> respective value
            --> insert the given 'element' value according to given 'comp' and removes the last one if
                there are more than k elements                                
        get_array: None --> list
            --> return the list of elements
'''
class KArray:

    def __init__(self, k):
        self.__array = []
        self.__k = k

    def insert(self, element, comp=lambda x: x[-1]):
        self.__array.append(element)
        self.__array = sorted(self.__array, key=comp)
        #if we have more than k elements, eliminate the last one
        if self.__k < len(self.__array):
            self.__array.pop()

    def get_array(self):
        return self.__array
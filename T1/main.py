'''
import sys
import cv2 as cv
import numpy as np
import os

data_path = '/data/cachorro.jpg'

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, data_path)

# Load an color image in grayscale
# img = cv.imread(data_path + 'gato.jpg', 0)
img = cv.imread('/data/cachorro.png', 0)
print(img)
a = True

if a:
	cv.imshow('image',img)
	cv.waitKey(0)
	cv.destroyAllWindows()
else:
	cv.namedWindow('image', cv.WINDOW_NORMAL)
	cv.imshow('image',img)
	cv.waitKey(0)
	cv.destroyAllWindows()
'''

from evaluar_v1 import *
from src.first_phase import *




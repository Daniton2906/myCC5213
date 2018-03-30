import sys
import cv2 as cv
import numpy as np
import os

data_path = 'data/'

# Load an color image in grayscale
img = cv.imread(data_path + 'gato.jpg', 0)

a = False

if a:
	cv.imshow('image',img)
	cv.waitKey(0)
	cv.destroyAllWindows()
else:
	cv.namedWindow('image', cv.WINDOW_NORMAL)
	cv.imshow('image',img)
	cv.waitKey(0)
	cv.destroyAllWindows()





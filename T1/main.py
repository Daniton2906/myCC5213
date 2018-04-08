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

from src.first_phase import *


if input('Codificar comerciales? Si(0) No(~0)') == '0':
    comerciales_list = []
    os.chdir("data/comerciales/")
    if not os.path.isdir(data_folder + "/comerc_txt/"):
        os.mkdir(data_folder + "/comerc_txt/")

    for filename in glob.glob('*.mpg'):
        comerciales_list.append(filename)

    print(len(comerciales_list))

    extractor1 = Extractor(comerciales_list, 3)
    r = extractor1.process_data(data_folder + "/comerciales/", margin={'top': 30, 'left': 43, 'bottom': 30, 'right': 43})
    print("Comerciales codificados...")
    extractor1.codify(data_folder + "/comerc_txt/")
    os.chdir("../../")

if input('Codificar television? Si(0) No(~0)') == '0':
    tele_list = []
    os.chdir("data/television/")
    if not os.path.isdir(data_folder + "/tele_txt/"):
        os.mkdir(data_folder + "/tele_txt/")

    for filename in glob.glob('*.mp4'):
        tele_list.append(filename)

    print(tele_list)

    extractor1 = Extractor(tele_list[0:1], 3)
    r = extractor1.process_data(data_folder + "/television/", max_frames=100000)
    print("Videos codificados...")
    extractor1.codify(data_folder + "/tele_txt/")


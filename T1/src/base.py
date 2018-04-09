import sys
import os
import cv2
import numpy as np
import easygui
import glob
import time

print("Usando OpenCV {} Python {}.{}.{}".format(cv2.__version__, sys.version_info.major, sys.version_info.minor, sys.version_info.micro))

# GLOBAL VARRIABLES
MAIN_FOLDER = "C:/Users/Daniel/Desktop/Semestre2018-1/multimedia/myCC5213/T1/"
DATA_FOLDER = "data/"
MAIN_DATA_FOLDER = MAIN_FOLDER + DATA_FOLDER
C_FOLDER = "comerciales/"
TV_FOLDER = "television/"
C_DESCRIP_FOLDER = "comerc_descriptors/"
TV_DESCRIP_FOLDER = "tv_descriptors/"
KNF_FOLDER = "k_nearest_frames/"
RESULTS_FOLDER = "results/"

FRAMES_PER_CELL = 10
K = 10


def show_frame(window_name, image, valorAbsoluto= False, escalarMin0Max255= False):
    if valorAbsoluto:
        image_abs = np.abs(image)
    else:
        image_abs = image
    if escalarMin0Max255:
        image_norm = cv2.normalize(image_abs, dst=None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    else:
        image_norm = image_abs
    cv2.imshow(window_name, image_norm)


def open_video(filename):
    if filename is None:
        filename = 0
    elif filename.isdigit():
        filename = int(filename)
    capture = None
    if isinstance(filename, int):
        print("abriendo camara {}".format(filename))
        capture = cv2.VideoCapture(filename)
    elif os.path.isfile(filename):
        print("abriendo archivo {}".format(filename))
        capture = cv2.VideoCapture(filename)
    if capture is None or not capture.isOpened():
        raise Exception("no puedo abrir video {}".format(filename))
    return capture


def load_filenames(files_folder, file_format, data_folder=DATA_FOLDER):
    new_list = []
    folder = data_folder + files_folder
    os.chdir(folder)

    for filename in glob.glob("*." + file_format):
        new_list.append(filename)

    os.chdir("../../")
    return new_list
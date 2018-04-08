import sys
import os
import cv2
import numpy as np
import easygui

print("Usando OpenCV {} Python {}.{}.{}".format(cv2.__version__, sys.version_info.major, sys.version_info.minor, sys.version_info.micro))


def show_frame(window_name, imagen, valorAbsoluto = False, escalarMin0Max255 = False):
    if valorAbsoluto:
        imagen_abs = np.abs(imagen)
    else:
        imagen_abs = imagen
    if escalarMin0Max255:
        imagen_norm = cv2.normalize(imagen_abs, dst=None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    else:
        imagen_norm = imagen_abs
    cv2.imshow(window_name, imagen_norm)


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

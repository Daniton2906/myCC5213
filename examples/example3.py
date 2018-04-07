from examples.base import *

def canny_ejemplo(filename, canny_threshold_1, canny_threshold_2):
    capture = abrir_video(filename)
    while capture.grab():
        retval, frame = capture.retrieve()
        if not retval:
            continue
        #convertir a gris
        frame_gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow("VIDEO", frame_gris)
        #calcular canny
        frame_canny = cv2.Canny(frame_gris, threshold1=canny_threshold_1, threshold2=canny_threshold_2)
        cv2.imshow("CANNY", frame_canny)
        #esperar por una tecla
        key = cv2.waitKey(1) & 0xFF
        if key == ord(' '):
            key = cv2.waitKey(0) & 0xFF
        if key == ord('q') or key == 27:
            break
    capture.release()
    cv2.destroyAllWindows()

canny_threshold_1 = 50
canny_threshold_2 = 200
#filename = easygui.fileopenbox(default="/", multiple=False)
filename = "0"

if filename is not None:
    canny_ejemplo(filename, canny_threshold_1, canny_threshold_2)
    print ("Presione una tecla para salir...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

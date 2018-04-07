from examples.base import *

def gaussians_diference_ejemplo(filename, sigma1, sigma2, threshold):
    capture = abrir_video(filename)
    while capture.grab():
        retval, frame = capture.retrieve()
        if not retval:
            continue
        #convertir a gris
        frame_gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow("VIDEO", frame_gris)
        #calcular DoG
        blur1 = cv2.GaussianBlur(frame_gris, (sigma1, sigma1), 0)
        blur2 = cv2.GaussianBlur(frame_gris, (sigma2, sigma2), 0)
        frame_diff = cv2.subtract(blur1, blur2)
        mostrar_frame("Diff", frame_diff, escalarMin0Max255=True)
        th, frame_bin = cv2.threshold(frame_diff, threshold, 255, cv2.THRESH_BINARY)
        mostrar_frame("BIN", frame_bin, escalarMin0Max255=True)
        #esperar por una tecla
        key = cv2.waitKey(1) & 0xFF
        if key == ord(' '):
            key = cv2.waitKey(0) & 0xFF
        if key == ord('q') or key == 27:
            break
    capture.release()
    cv2.destroyAllWindows()

sigma1 = 5
sigma2 = 13
threshold = 4
filename = easygui.fileopenbox(default="/", multiple=False)

gaussians_diference_ejemplo(filename, sigma1, sigma2, threshold)

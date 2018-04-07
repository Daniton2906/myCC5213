from examples.base import *

def otsu_ejemplo(filename):
    print("abriendo {}".format(filename))
    imagen_color = cv2.imread(filename, cv2.IMREAD_COLOR)
    #print(imagen_color.shape)
    for row in imagen_color:
        print(row)
    if imagen_color is None:
        print ("error abriendo {}".format(filename))
        return
    imagen_gris = cv2.cvtColor(imagen_color, cv2.COLOR_BGR2GRAY)
    threshold, imagen_bin = cv2.threshold(imagen_gris, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    window_name = os.path.basename(filename)
    #cv2.imshow(window_name, imagen_color)
    cv2.imshow(window_name + " GRIS", imagen_gris)
    #cv2.imshow(window_name + " BINARIA", imagen_bin)
    print ("{}: size={} threshold_otsu={}".format(window_name, imagen_color.shape, threshold))

'''
filenames = easygui.fileopenbox(default="/", multiple=True)

if filenames is not None:
    for filename in filenames:
        otsu_ejemplo(filename)
    print("Presione una tecla para salir...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()
'''

squall = "C:/Users/Daniel/Desktop/squall.jpg"
otsu_ejemplo(squall)
print("Presione una tecla para salir...")
cv2.waitKey(0)
cv2.destroyAllWindows()

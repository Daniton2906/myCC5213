from src.base import *
from src.first_phase import Extractor, HistDescriptor, IntensityVectorDescriptor
from src.second_phase import Comparator, Loader
from src.third_phase import Detector

# Global variables
FRAMES_PER_CELL = 10
K = 10
RESIZE = (320, 180)  #(160, 90), (432, 768)
FPS_RATE = 30
TOLERANCE = 70
EPSILON = 5
DESCRIP_MANAGER = IntensityVectorDescriptor(20, 11)  # HistDescriptor(16, 4, 4, RESIZE)


def main():
    # receive input arguments
    if len(sys.argv) < 3:
        print("CC5213 - Tarea 1")
        print("Uso: {} [TV filename] [carpeta comerciales]".format(sys.argv[0]))
        sys.exit(1)

    # Split between tv folder path and tv file name
    tmp_str = sys.argv[1].replace("\\", "/")
    tmp_list = tmp_str.split("/")

    tv_filename = tmp_list[-1]

    tv_folder = tmp_list[0]
    for s in tmp_list[1:-1]:
        tv_folder = tv_folder + "/" + s
    tv_folder = tv_folder + "/"

    comerc_folder = sys.argv[2]

    # Counter for time
    global_counter = 0

    # Define actions to take on
    seq = '0000'
    if input('Hacer todo? Si(1) No(~1): ') == '1':
        seq = '1111'
    else:
        seq = input('Ingrese secuencia de largo 4 de que hacer: Si(1) No(~1): ')

    # Calculate descriptors for comerciales
    if seq[0] == '1':
        print("Codificando comerciales...")
        start = time.time()

        comerciales_list = Loader.load_filenames(comerc_folder, "mpg")
        print("Comerciales encontrados: {}".format(len(comerciales_list)))

        extractor1 = Extractor(comerciales_list, FRAMES_PER_CELL)
        r = extractor1.process_data(DESCRIP_MANAGER, comerc_folder)  # , margin={'top': 30, 'left': 43, 'bottom': 30, 'right': 43})

        Loader.clean_data(C_DESCRIP_FOLDER)
        extractor1.codify(C_DESCRIP_FOLDER)

        end = time.time()
        global_counter += int(end - start)
        print("Comerciales codificados en {}s...".format(int(end - start)))

    # Calculate descriptors for television
    if seq[1] == '1':
        print("Codificando television...")
        start = time.time()

        #tele_list = Loader.load_filenames(TV_FOLDER, "mp4")
        #print("Videos de televison encontrados: {}".format(tele_list))

        extractor2 = Extractor([tv_filename], FRAMES_PER_CELL)
        r = extractor2.process_data(DESCRIP_MANAGER, tv_folder)  # max_frames=1500, rsize=RESIZE)

        Loader.clean_data(TV_DESCRIP_FOLDER)
        extractor2.codify(TV_DESCRIP_FOLDER)

        end = time.time()
        global_counter += int(end - start)
        print("Videos codificados en {}s...".format(int(end - start)))

    # Calculate k-nearest frames for each television's frame
    if seq[2] == '1':
        print("Calculando KNFs...")
        start = time.time()

        comerc_descriptor_list = Loader.load_filenames(C_DESCRIP_FOLDER, "txt")
        tele_list = Loader.load_filenames(TV_DESCRIP_FOLDER, "txt")

        comparator1 = Comparator(comerc_descriptor_list)
        r = comparator1.load_data(C_DESCRIP_FOLDER)

        Loader.clean_data(KNF_FOLDER)
        for tele in tele_list:
            print("calculando KNFs (k = {}) para {}...".format(K, tele))
            result = comparator1.k_nearest_frames(K, DESCRIP_MANAGER, tele, TV_DESCRIP_FOLDER)
            comparator1.write_on_memory(result, tele, KNF_FOLDER)

        end = time.time()
        global_counter += int(end - start)
        print("{} frames más cercanos calculados en {}s...".format(K, int(end - start)))

    # Detect comerciales
    if seq[3] == '1':
        print("Detectando colisiones...")
        start = time.time()

        knf_list = Loader.load_filenames(KNF_FOLDER, "txt")
        comerc_descriptor_list = Loader.load_filenames(C_DESCRIP_FOLDER, "txt")

        detector = Detector(knf_list, K, comerc_descriptor_list)
        detector.load_data(KNF_FOLDER)
        matches = detector.detect_match(EPSILON, TOLERANCE)

        detector.filter_write_results("detecciones.txt", RESULTS_FOLDER, EPSILON, FPS_RATE//FRAMES_PER_CELL)

        end = time.time()
        global_counter += int(end - start)
        print("Detecciones identificadas en {}s...".format(int(end - start)))

    print("Tiempo total: {}s...".format(global_counter))

if __name__ == "__main__":
    main()



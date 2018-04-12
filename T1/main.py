from src.base import *
from src.first_phase import Extractor, HistDescriptor, IntensityVectorDescriptor
from src.second_phase import Comparator
from src.third_phase import Detector

# Global variables
FRAMES_PER_CELL = 10
K = 10
RESIZE = (320, 180)  #(160, 90), (432, 768)
FPS_RATE = 30
TOLERANCE = 70
EPSILON = 5
DESCRIP_MANAGER = IntensityVectorDescriptor(20, 11)  # HistDescriptor(16, 4, 4, RESIZE)

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

    comerciales_list = load_filenames(C_FOLDER, "mpg")
    print("Comerciales encontrados: {}".format(len(comerciales_list)))

    extractor1 = Extractor(comerciales_list, FRAMES_PER_CELL)
    r = extractor1.process_data(MAIN_DATA_FOLDER + C_FOLDER, DESCRIP_MANAGER)  # , margin={'top': 30, 'left': 43, 'bottom': 30, 'right': 43})
    end = time.time(); global_counter += int(end - start)
    print("Comerciales codificados en {}s...".format(int(end - start)))

    extractor1.codify(MAIN_FOLDER + DATA_FOLDER + C_DESCRIP_FOLDER)

# Calculate descriptors for television
if seq[1] == '1':
    print("Codificando television...")
    start = time.time()

    tele_list = load_filenames(TV_FOLDER, "mp4")
    print("Videos de televison encontrados: {}".format(tele_list))

    extractor2 = Extractor(tele_list, FRAMES_PER_CELL)
    r = extractor2.process_data(MAIN_DATA_FOLDER + TV_FOLDER, DESCRIP_MANAGER)  # max_frames=1500, rsize=RESIZE)
    extractor2.codify(MAIN_FOLDER + DATA_FOLDER + TV_DESCRIP_FOLDER)

    end = time.time(); global_counter += int(end - start)
    print("Videos codificados en {}s...".format(int(end - start)))

# Calculate k-nearest frames for each television's frame
if seq[2] == '1':
    print("Calculando KNFs...")
    start = time.time()

    comerc_descriptor_list = load_filenames(C_DESCRIP_FOLDER, "txt")
    tele_list = load_filenames(TV_DESCRIP_FOLDER, "txt")

    comparator1 = Comparator(comerc_descriptor_list)
    r = comparator1.load_data(MAIN_DATA_FOLDER + C_DESCRIP_FOLDER)

    for tele in tele_list:
        print("calculando KNFs (k = {}) para {}...".format(K, tele))
        result = comparator1.k_nearest_frames(K, DESCRIP_MANAGER, tele, DATA_FOLDER + TV_DESCRIP_FOLDER)
        comparator1.write_on_memory(result, tele, DATA_FOLDER + KNF_FOLDER)

    end = time.time(); global_counter += int(end - start)
    print("{} frames más cercanos calculados en {}s...".format(K, int(end - start)))

# Detect comerciales
if seq[3] == '1':
    print("Detectando colisiones...")
    start = time.time()

    knf_list = load_filenames(KNF_FOLDER, "txt")
    comerc_descriptor_list = load_filenames(C_DESCRIP_FOLDER, "txt")

    detector = Detector(knf_list, K, comerc_descriptor_list)
    detector.load_data(MAIN_DATA_FOLDER + KNF_FOLDER)
    matches = detector.detect_match(EPSILON, TOLERANCE)

    detector.filter_write_results("results.txt", MAIN_DATA_FOLDER + RESULTS_FOLDER, EPSILON, FPS_RATE//FRAMES_PER_CELL)

    end = time.time(); global_counter += int(end - start)
    print("Detecciones identificadas en {}s...".format(int(end - start)))

print("Tiempo total: {}s...".format(global_counter))




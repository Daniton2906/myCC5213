from src.base import *
from src.first_phase import Extractor
from src.second_phase import Comparator
from src.third_phase import Detector

# s = (320, 180)
# 432, 768
global_counter = 0

DO_ALL = False
seq = '0000'
if input('Hacer todo? Si(1) No(~1): ') == '1':
    DO_ALL = True
else:
    seq = input('Ingrese secuencia de largo 4 de que hacer: Si(1) No(~1): ')
# Calculate descriptors for comerciales
if DO_ALL or seq[0] == '1':
    print("Codificando comerciales...")
    start = time.time()
    comerciales_list = load_filenames(C_FOLDER, "mpg")
    print("Comerciales encontrados: {}".format(len(comerciales_list)))
    extractor1 = Extractor(comerciales_list, FRAMES_PER_CELL)
    r = extractor1.process_data(MAIN_DATA_FOLDER + C_FOLDER, rsize=RESIZE) #, margin={'top': 30, 'left': 43, 'bottom': 30, 'right': 43})
    end = time.time(); global_counter += int(end - start)
    print("Comerciales codificados en {}s...".format(int(end - start)))
    extractor1.codify(MAIN_FOLDER + DATA_FOLDER + C_DESCRIP_FOLDER)


# Calculate descriptors for television
if DO_ALL or seq[1] == '1':
    print("Codificando television...")
    start = time.time()
    tele_list = load_filenames(TV_FOLDER, "mp4")
    print("Videos de televison encontrados: {}".format(tele_list))
    extractor2 = Extractor(tele_list, FRAMES_PER_CELL)
    r = extractor2.process_data(MAIN_DATA_FOLDER + TV_FOLDER, rsize=RESIZE)#max_frames=1500, rsize=RESIZE)
    end = time.time(); global_counter += int(end - start)
    print("Videos codificados en {}s...".format(int(end - start)))
    extractor2.codify(MAIN_FOLDER + DATA_FOLDER + TV_DESCRIP_FOLDER)

# Calculate k-nearest frames for each television's frame
if DO_ALL or seq[2] == '1':
    print("Calculando KNFs...")
    comerc_descriptor_list = load_filenames(C_DESCRIP_FOLDER, "txt")
    fixed_list = comerc_descriptor_list #[10:11] + comerc_descriptor_list[-3:]
    #print(fixed_list)

    tele_list = load_filenames(TV_DESCRIP_FOLDER, "txt")
    #print(tele_list)

    comparator1 = Comparator(fixed_list)
    start = time.time()
    r = comparator1.load_data(MAIN_DATA_FOLDER + C_DESCRIP_FOLDER)
    for tele in tele_list[0:2]:
        print("calculando KNFs para {}...".format(tele))
        result = comparator1.k_nearest_frames(K, tele, DATA_FOLDER + TV_DESCRIP_FOLDER)
        print(result.shape)
        comparator1.write_on_memory(result, tele, DATA_FOLDER + KNF_FOLDER)
    end = time.time(); global_counter += int(end - start)
    print("{} frames más cercanos calculados en {}s...".format(K, int(end - start)))

# Detect comerciales
if DO_ALL or seq[4] == '1':
    print("Detectando colisiones...")
    start = time.time()
    knf_list = load_filenames(KNF_FOLDER, "txt")
    comerc_descriptor_list = load_filenames(C_DESCRIP_FOLDER, "txt")

    #print(len(knf_list))

    detector = Detector(knf_list, K, comerc_descriptor_list)
    detector.load_data(MAIN_DATA_FOLDER + KNF_FOLDER)
    matches = detector.detect_match()
    #for r in matches[0]:
    #    print(r)

    detector.filter_write_results("results.txt", MAIN_DATA_FOLDER + RESULTS_FOLDER)
    end = time.time(); global_counter += int(end - start)
    print("Detecciones identificadas en {}s...".format(int(end - start)))

print("Tiempo total: {}s...".format(global_counter))




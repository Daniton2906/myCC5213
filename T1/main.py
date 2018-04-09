from src.base import *
from src.first_phase import Extractor
from src.second_phase import Comparator
from src.third_phase import Detector

JUMP = True
# s = (320, 180)
# 432, 768
RESIZE = (160, 90)
# Calculate descriptors for comerciales
if JUMP and input('Codificar comerciales? Si(1) No(~1)') == '1':
    start = time.time()
    comerciales_list = load_filenames(C_FOLDER, "mpg")
    print(len(comerciales_list))
    extractor1 = Extractor(comerciales_list, FRAMES_PER_CELL)
    r = extractor1.process_data(MAIN_DATA_FOLDER + C_FOLDER, rsize=RESIZE) #, margin={'top': 30, 'left': 43, 'bottom': 30, 'right': 43})
    end = time.time()
    print("Comerciales codificados en {}s...".format(end - start))
    extractor1.codify(MAIN_FOLDER + DATA_FOLDER + C_DESCRIP_FOLDER)


# Calculate descriptors for television
if JUMP and input('Codificar television? Si(1) No(~1)') == '1':

    start = time.time()
    tele_list = load_filenames(TV_FOLDER, "mp4")
    print(tele_list)
    extractor2 = Extractor(tele_list[0:1], FRAMES_PER_CELL)
    r = extractor2.process_data(MAIN_DATA_FOLDER + TV_FOLDER, max_frames=1500, rsize=RESIZE)
    end = time.time()
    print("Videos codificados en {}s...".format(int(end - start)))
    extractor2.codify(MAIN_FOLDER + DATA_FOLDER + TV_DESCRIP_FOLDER)

# Calculate k-nearest frames for each television's frame
if JUMP and input('Calcular KNFs? Si(1) No(~1)') == '1':
    comerc_descriptor_list = load_filenames(C_DESCRIP_FOLDER, "txt")
    fixed_list = comerc_descriptor_list[10:11] + comerc_descriptor_list[-3:]
    print(fixed_list)

    tele_list = load_filenames(TV_DESCRIP_FOLDER, "txt")
    print(tele_list)

    comparator1 = Comparator(fixed_list)
    start = time.time()
    r = comparator1.load_data(MAIN_DATA_FOLDER + C_DESCRIP_FOLDER)
    for tele in tele_list[0:1]:
        result = comparator1.k_nearest_frames(K, tele, DATA_FOLDER + TV_DESCRIP_FOLDER)
        print(result.shape)
        comparator1.write_on_memory(result, tele, DATA_FOLDER + KNF_FOLDER)
    end = time.time()
    print("{} frames más cercanos calculados en {}s...".format(K, int(end - start)))

# Detect comerciales
if JUMP and input('Detectar comerciales? Si(1) No(~1)') == '1':
    knf_list = load_filenames(KNF_FOLDER, "txt")
    print(len(knf_list))

    detector = Detector(knf_list, K)
    r = detector.load_data(MAIN_DATA_FOLDER + KNF_FOLDER)
    r2 = detector.detect_match()
    print(len(r2))
    for rr in r2:
        print(rr)




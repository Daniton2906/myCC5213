from src.base import *
from src.first_phase import Extractor
from src.second_phase import Comparator

JUMP = False

if JUMP and input('Codificar comerciales? Si(0) No(~0)') == '0':
    comerciales_list = load_filenames(C_FOLDER, "mpg")
    print(len(comerciales_list))
    extractor1 = Extractor(comerciales_list, FRAMES_PER_CELL)
    r = extractor1.process_data(MAIN_FOLDER + DATA_FOLDER + C_FOLDER) #, margin={'top': 30, 'left': 43, 'bottom': 30, 'right': 43})
    print("Comerciales codificados...")
    extractor1.codify(MAIN_FOLDER + DATA_FOLDER + C_DESCRIP_FOLDER)

if JUMP and input('Codificar television? Si(0) No(~0)') == '0':
    tele_list = load_filenames(TV_FOLDER, "mp4")
    print(tele_list)
    extractor2 = Extractor(tele_list[0:1], FRAMES_PER_CELL)
    r = extractor2.process_data(MAIN_FOLDER + DATA_FOLDER + TV_FOLDER, max_frames=50000)
    print("Videos codificados...")
    extractor2.codify(MAIN_FOLDER + DATA_FOLDER + TV_DESCRIP_FOLDER)

if JUMP and input('Calcular KNFs? Si(0) No(~0)') == '0':
    comerc_descriptor_list = load_filenames(C_DESCRIP_FOLDER, "txt")
    print(comerc_descriptor_list)

    tele_list = load_filenames(TV_DESCRIP_FOLDER, "txt")
    print(tele_list)

    comparator1 = Comparator(comerciales_list[0:3])
    r = comparator1.load_data(DATA_FOLDER + C_DESCRIP_FOLDER)
    for tele in tele_list[0:1]:
        result = comparator1.k_nearest_frames(K, tele, DATA_FOLDER + TV_DESCRIP_FOLDER)
        print(result.shape)
        comparator1.write_on_memory(result, tele, DATA_FOLDER + KNF_FOLDER)

    print("{} frames más cercanos calculados...".format(K))

from __future__ import print_function

import os
import sys
import scipy.io.wavfile
import time

#from pyAudioAnalysis import audioTrainTest as aT
from ffmpeg import Error

from tools.compare_phase import Comparator
from tools.descriptor_tools import DescriptorManager
from tools.detect_phase import Detector
from tools.media_tools import RawManager


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


FRAMES_PER_CELL = 10
K = 10
RESIZE = (320, 180)  # (160, 90), (432, 768)

video_folder = "videos"
output_folder = "out"

one_piece_video = "[RedLineSP] Episodio 01 ¡Soy Luffy! ¡El hombre que se convertirá en el Rey de los Piratas!»"

data_path = os.path.join(os.getcwd(), "data")

input_filename = os.path.join(data_path, video_folder, "episode0_run.mp4")
input_one_piece = os.path.join(data_path, video_folder, one_piece_video + ".mp4")

input_cut1 = os.path.join(data_path, video_folder, "cut1.mp4")
output_cut1 = os.path.join(data_path, output_folder, "cuts", "cut1.wav")

output_mp4 = os.path.join(data_path, output_folder, "output.mp4")
output_mp3 = os.path.join(data_path, output_folder, "output.mp3")
output_wav = os.path.join(data_path, output_folder, "output.wav")
output_raw = os.path.join(data_path, output_folder, "output.raw")
output_one_piece = os.path.join(data_path, output_folder, one_piece_video + ".mp3")


absolute_data_folder = os.path.join(data_path, video_folder)

cuts_videos = os.path.join(data_path, output_folder, "cuts")
wav_videos_001_100 = os.path.join(data_path, output_folder, "wavs_1_100")
wav_videos_101_200 = os.path.join(data_path, output_folder, "wavs_101_200")
wav_videos_201_300 = os.path.join(data_path, output_folder, "wavs_201_300")
wav_videos_301_400 = os.path.join(data_path, output_folder, "wavs_301_400")
wav_videos_401_500 = os.path.join(data_path, output_folder, "wavs_401_500")
wav_videos_501_600 = os.path.join(data_path, output_folder, "wavs_501_600")
wav_videos_601_700 = os.path.join(data_path, output_folder, "wavs_601_700")
wav_videos_701_800 = os.path.join(data_path, output_folder, "wavs_701_800")

wavs_folder = [wav_videos_001_100, wav_videos_101_200, wav_videos_201_300, wav_videos_301_400, wav_videos_401_500, wav_videos_501_600, wav_videos_601_700, wav_videos_701_800]

one_piece_folder_001_100 = "F:\Peliculas y Series\One Piece\One Piece 1 - 100"
one_piece_folder_101_200 = "F:\Peliculas y Series\One Piece\One Piece 101 - 200"
one_piece_folder_201_300 = "F:\Peliculas y Series\One Piece\One Piece 201 - 300"
one_piece_folder_301_400 = "F:\Peliculas y Series\One Piece\One Piece 301 - 400"
one_piece_folder_401_500 = "F:\Peliculas y Series\One Piece\One Piece 401 - 500"
one_piece_folder_501_600 = "F:\Peliculas y Series\One Piece\One Piece 501 - 600"
one_piece_folder_601_700 = "F:\Peliculas y Series\One Piece\One Piece 601 - 700"
one_piece_folder_701_800 = "F:\Peliculas y Series\One Piece\One Piece 701 - 800"


def get_seconds(seconds, minutes=0, hours=0):
    return seconds + 60 * (minutes + 60 * hours)


def main():
    # receive input arguments
    if False and len(sys.argv) >= 3:
        print("CC5213 - Proyecto")
        print("Uso: {} path_extracto path_capitulos".format(sys.argv[0]))
        sys.exit(1)

    if len(sys.argv) == 4:
        my_cut_list = [sys.argv[1]]
        inicio = int(sys.argv[2])
        final = int(sys.argv[3])
    else:
        my_cut_list = os.listdir(os.path.join(data_path, video_folder, "cuts"))
        inicio = 0
        final = 10

    print(os.getcwd())
    print(os.listdir("."))
    try:
        # RawManager.get_all_wavs(one_piece_folder_001_100, wav_videos_1_100)
        # RawManager.get_all_wavs(one_piece_folder_101_200, wav_videos_101_200)
        # RawManager.get_all_wavs(one_piece_folder_201_300, wav_videos_201_300)
        # RawManager.get_all_wavs(one_piece_folder_301_400, wav_videos_301_400)
        # RawManager.get_all_wavs(one_piece_folder_401_500, wav_videos_401_500)
        # RawManager.get_all_wavs(one_piece_folder_501_600, wav_videos_501_600)
        # RawManager.get_all_wavs(one_piece_folder_601_700, wav_videos_601_700)
        # RawManager.get_all_wavs(one_piece_folder_701_800, wav_videos_701_800)
        pass
    except Error as e:
        eprint()

    s = get_seconds(13, minutes=13)
    print(s)
    all_episodes = []
    for wav_folder in wavs_folder[:1]:
        all_episodes.extend(os.listdir(wav_folder))
    print(len(all_episodes))

    # RawManager.encode(wav_videos_001_100, os.path.join(data_path, output_folder, "wavs_1_100.txt"))
    # RawManager.decode(wav_videos_001_100, os.path.join(data_path, output_folder, "wavs_1_100.txt"))


    # cap_1 = os.path.join(wav_videos_1_100, caps_list[0])
    # cap_2 = os.path.join(wav_videos_1_100, caps_list[1])

    # sample_rate0, signal0 = scipy.io.wavfile.read(cap_1)  # File assumed to be in the same directory
    # sample_rate1, signal1 = scipy.io.wavfile.read(cap_2)  # File assumed to be in the same directory
    # sample_rate2, signal2 = scipy.io.wavfile.read(output_cut1)  # File assumed to be in the same directory

    # descrip0 = DescriptorManager(sample_rate0, signal0, RawManager.get_name(caps_list[0]))
    # descrip1 = DescriptorManager(sample_rate1, signal1, RawManager.get_name(caps_list[1]))
    # descrip2 = DescriptorManager(sample_rate2, signal2, "cut1")

    current_milli_time = lambda: int(round(time.time() * 1000))

    for cut in my_cut_list:
        print(cut)
        cut_name = RawManager.get_name(cut)
        output_cut = os.path.join(data_path, output_folder, "cuts", cut_name + ".wav")
        if not os.path.exists(output_cut):
            input_cut1 = os.path.join(data_path, video_folder, "cuts", cut)
            print(input_cut1)
            RawManager.video_to_wav(input_cut1, output_cut)
        sample_rate, signal = scipy.io.wavfile.read(output_cut)  # File assumed to be in the same directory
        cut_descrip = DescriptorManager(sample_rate, signal, cut_name)

        k = 5
        caps_list = all_episodes[inicio:final + 1]
        c = Comparator(caps_list)
        s = 0
        for wav_folder in wavs_folder[:1]:
            c.load_data(wav_folder)
        d = Detector([cut_name], k)

        n_cut_name = cut_name + "_" + str(len(caps_list))
        if os.path.exists(os.path.join(output_folder, "knn_" + n_cut_name + ".txt")):
            d.load_data(output_folder)
        else:
            start = current_milli_time()
            box = c.k_nearest_frames(k, cut_descrip)
            print("{}-nn time for {}: {}s".format(k, n_cut_name, (current_milli_time() - start)/1000))
            c.write_on_memory(box, k, n_cut_name, output_folder)
            # print(box)
            d.append_kbox(box)

        matches = d.detect_match(0, 90)
        d.write_results("my_results_" + n_cut_name + ".txt", output_folder, debug=True, episodes=final-inicio)
        '''
        for myMatch in matches:
            for match in myMatch:
                for frame in match:
                    print(str(frame))
            print("-----")
        return
        '''

    '''
    #descrip0.save_mfcc()
    #descrip1.save_mfcc()
    #print(descrip1.get_mfcc().shape)

    print(signal0.shape)
    print(signal1.shape)
    print(signal2.shape)
    print(DescriptorManager.get_match(descrip0, descrip2))
    print()
    print(DescriptorManager.get_match(descrip1, descrip2))
    
    # mfcc1 = DescriptorManager.get_mfcc(output_wav, start=s, seconds=3.5)
    # mfcc2 = DescriptorManager.get_mfcc(output_cut1, start=0, seconds=3.5)


    # mfcc2 = np.random.randint(-2**15, 2**15 - 1, size=(300, 12), dtype=np.int16)

    # print(mfcc1.shape)
    # print(mfcc2.shape)

    # X = []
    # X.append(np.mean(mfcc[int(num_ceps / 10):int(num_ceps * 9 / 10)], axis=0))
    # print(mfcc1[356])
    # print(mfcc1[455])
    # print(euclidean(mfcc1[356], mfcc1[455]))

    # dist = DescriptorManager.mfcc_distance(mfcc1, mfcc2)
    # print('Normalized distance between the two sounds:', dist)


    #Vx = np.array(X)
    #print(Vx.shape)


    # print(signal)
    # print(sample_rate)
    '''


if __name__ == "__main__":
    main()

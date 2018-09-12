import os
import ffmpeg


class RawManager:

    @staticmethod
    def get_name(filename, sep="."):
        return "".join(filename.split(sep)[:-1])

    @staticmethod
    def encode(wav_folder, filename):
        caps_list = os.listdir(wav_folder)
        codify_caps = filename
        fd = open(codify_caps, "w")
        for i, cap in enumerate(caps_list, start=1):
            new_name = str(i) + ".wav"
            fd.write("{} \t {}\n".format(new_name, cap))
            os.rename(os.path.join(wav_folder, cap), os.path.join(wav_folder, new_name))
            caps_list[i - 1] = new_name
        fd.close()
        return caps_list

    @staticmethod
    def decode(wav_folder, filename):
        caps_list = []
        codify_caps = filename
        fd = open(codify_caps, "r")
        line = fd.readline()[:-1]
        while line != "":
            tline = line.split("\t")
            i = tline[0]
            cap = tline[1]
            os.rename(os.path.join(wav_folder, i), os.path.join(wav_folder, cap))
            line = fd.readline()[:-1]
            caps_list.append(cap)
        fd.close()
        return caps_list

    @staticmethod
    def get_all_wavs(video_folder, output_folder):
        cwd = os.getcwd()
        # os.chdir()
        print(output_folder)
        if not os.path.exists(output_folder):
            os.mkdir(output_folder)
        n = 0
        files = os.listdir(video_folder)
        for file in files:
            if ".mp4" in file or '.mkv' in file:
                filename = os.path.join(video_folder, file)
                print(filename)
                output = os.path.join(output_folder, RawManager.get_name(file).replace(" ", "_") + ".wav")
                print(output)
                RawManager.video_to_wav(filename, output)
        os.chdir(cwd)
        return n


    @staticmethod
    def video_to_raw(video_path, out_path, cwd="."):
        out, _ = (ffmpeg
                  .input(video_path)
                  .output(out_path, format='s16le', acodec='pcm_s16le', ac=1, ar='16k')
                  .overwrite_output()
                  .run(capture_stdout=True)
                  )
        return out

    @staticmethod
    def video_to_wav(video_path, out_path, cwd="."):
        out, _ = (ffmpeg
                  .input(video_path)
                  .output(out_path, format='wav', ac=1, ar='16k')
                  .overwrite_output()
                  .run(capture_stdout=True)
                  )
        return out

    @staticmethod
    def raw_to_numpy(audio_raw):
        pass

    @staticmethod
    def get_sub_video(video_path):
        in_file = ffmpeg.input('input.mp4')
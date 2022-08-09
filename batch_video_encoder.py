import json
import shutil
import os
import sys
from collections import deque


class BatchVideoEncoder:
    def __init__(self):
        self.file_path = "C:\\Users\\xxxx\\Desktop\\"
        self.ffmpeg_config = "echo y | ffmpeg -i  \"{}\" -c:a aac -ac 2 -c:v hevc_nvenc -profile main10 -preset slow " \
                             "-rc vbr -cq 16 \"{}\" "
        self.encode_name = "-Encode"
        self.encode_format = ".mkv"
        # Not suggest to choose FALSE, It may cause losing original files
        self.new_dir_to_encode = True

    def encode_start(self):
        if not os.path.exists("Recovery.json"):
            with open("Recovery.json", "w", encoding="utf-8") as recovery_file:
                print("Recovery file is not exist, Creat a new one in current directory")
                wait_list = self.get_every_video_path(self.get_save_dir(self.file_path))
        else:
            rec_flag = input("Recovery file is exist, Try recover the encode queue?[y/n]: ")
            if rec_flag == "y" or rec_flag == "Y":
                with open("Recovery.json", "r", encoding="utf-8") as recovery_file:
                    try:
                        wait_list = json.load(recovery_file)
                    except IOError:
                        print("Recovery file is broken, Please check it and restart the program")
            else:
                print("Please Delete the Recovery.json in current directory and restart the program")
                sys.exit()

        self.encode_queue(wait_list)

    # Encode the videos in the queue
    def encode_queue(self, wait_list):
        encode_max_num = len(wait_list)
        cur_num = 0
        encode_queue = deque(wait_list)
        with open("Recovery.json", "w", encoding="utf-8") as recovery_file:
            json.dump(wait_list, recovery_file, ensure_ascii=False)

        while encode_queue:
            cur_num += 1
            source_path = encode_queue.popleft()
            print("No.", cur_num, "in encode queue...", encode_max_num, "videos in total")

            encode_name = source_path.rsplit(".", 1)[0] + self.encode_name + self.encode_format
            ffmpeg_encode = self.ffmpeg_config.format(source_path, encode_name)

            print(ffmpeg_encode)
            is_run = os.system(ffmpeg_encode)
            if is_run != 0:
                print("Maybe ffmpeg got error, Please check it")
            os.remove(source_path)
            with open("Recovery.json", "w", encoding="utf-8") as recovery_file:
                encode_queue_list = list(encode_queue)
                json.dump(encode_queue_list, recovery_file, ensure_ascii=False)

        print("Done! Encoded", encode_max_num, "videos this time")
        os.remove("Recovery.json")

    # Get all the video files in the directory
    def get_every_video_path(self, encode_path):
        filelist = []
        for root, _, files in os.walk(encode_path, topdown=False):
            for name in files:
                filelist.append(os.path.join(root, name))
        res = []
        for f in filelist:
            if self.is_video(f):
                f = os.path.abspath(f)
                res.append(f)
        return res

    # Create a new directory to save the encoded videos, and copy the original stuff to the new directory
    # Or just return the original directory if you want to encode in the original directory (Not suggest)
    def get_save_dir(self, file_path):
        if not self.new_dir_to_encode:
            return file_path
        target_path = os.path.abspath(file_path) + "__" + self.encode_name
        if os.path.exists(target_path):
            shutil.rmtree(target_path)
        shutil.copytree(os.path.abspath(file_path), os.path.abspath(target_path))
        return target_path

    def is_video(self, video_path):
        video_suffix_list = ["MKV", "MP4", "WMV", "WEBM", "M2TS", "ASF", "ASX", "RM", "RMVB", "3GP", "MOV", "M4V",
                             "AVI", "FLV", "VOB", "MTS", "TS", "M2T", "M2V", "MPG", "MPEG", "MPG2", "MPE"]
        # uppercase format name
        return True if video_path.rsplit(".", 1)[-1].upper() in video_suffix_list else False


if __name__ == "__main__":
    worker_01 = BatchVideoEncoder()
    worker_01.ffmpeg_config = "echo y | ffmpeg -hwaccel cuda -hwaccel_output_format cuda -extra_hw_frames 8 -i  \"{}\"" \
                              " -vf \"hwdownload,format=nv12\" -c:a aac -ac 2 -c:v hevc_nvenc -profile main10 -pix_fmt" \
                              " p010le -preset slow -rc vbr -cq 16 \"{}\" "
    worker_01.encode_name = "-Encode"
    worker_01.encode_format = ".mkv"
    worker_01.new_dir_to_encode = False
    if os.path.exists("Recovery.json"):
        worker_01.encode_start()
    else:
        print("Please set the ffmpeg config in \" __name__ == \"__main__\" \" before start")
        worker_01.file_path = input("Please input the directory you want to bulk encode: ")
        print("Encode Name: {} || Encode Format: {} || New Dir to Encode?: {}".format(worker_01.encode_name,
                                                                                      worker_01.encode_format,
                                                                                      worker_01.new_dir_to_encode))
        print("FFmpeg Parameters: {}".format(worker_01.ffmpeg_config))
        input("Get Ready? Press Enter to encode!")
        worker_01.encode_start()

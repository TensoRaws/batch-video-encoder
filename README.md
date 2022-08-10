# batch-video-encoder

* Encode all videos in folder at a time with ffmpeg commads 
* The original non-video-files will be retained in relative path

### Prerequisites

The following dependencies are recommended

* **[Python](https://www.python.org/downloads/)**  3.6 or above
* **[FFmpeg](https://www.ffmpeg.org/)** 1.0 or above

## Getting Started

#### IN ` if __name__ == "__main__": `

* set ffmpeg config like ` echo y | ffmpeg -i  \"{}\" -c:a aac -ac 2 -c:v hevc_nvenc -profile main10 \"{}\" ` 
* `\"{}\"` is the input and output file path

### Example

```
if __name__ == "__main__":
    worker_01 = BatchVideoEncoder()
    worker_01.ffmpeg_config = "echo y | ffmpeg -hwaccel cuda -hwaccel_output_format cuda -extra_hw_frames 8 -i  \"{}\"" \
                              " -vf \"hwdownload,format=nv12\" -c:a aac -ac 2 -c:v hevc_nvenc -profile main10 -pix_fmt" \
                              " p010le -preset slow -rc vbr -cq 16 \"{}\" "
    worker_01.encode_name = "-Encode"
    worker_01.encode_format = ".mkv"
    # Creat a new folder, copy then encode. Not suggest to choose FALSE, It may cause losing original files
    worker_01.new_dir_to_encode = True
```


import glob
import os
import re
import subprocess

from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def __init__(self):
        super().__init__()
        self.codecs = ['mpeg4', 'hevc', 'h264']

    def handle(self, *args, **options):

        videos = glob.glob('/app/convert/*')

        for path in videos:

            new_path = re.sub('[^0-9a-zA-Z_./\s]+', '', path)
            new_path = new_path.replace(" ", "_")
            # new_path = new_path.replace(".", "_")
            if new_path != path:
                os.rename(path, new_path)
                print("Moved", path, "to", new_path)

        videos = glob.glob('/app/convert/*')
        for i, path in enumerate(videos):

            file_name = os.path.basename(path)
            ext = file_name.split(".")[-1]
            name = file_name.replace("." + ext, "")

            if ext in ["srt", "vtt"]:
                print("Skipping", path)
                continue

            process = subprocess.Popen(
                "ffprobe -v error -select_streams v:0 -show_entries stream=cod"
                "ec_name -of default=noprint_wrappers=1:nokey=1 {}".format(
                    path),
                shell=True,
                stdout=subprocess.PIPE
            )
            codec, err = process.communicate()

            codec = codec.decode("UTF-8")
            codec = codec.replace("\n", "")
            codec = codec.strip()

            if codec not in self.codecs:
                print("Codec {} not supported in file {}".format(codec, path))
                continue

            video_stream = "0:0"
            audio_stream = None

            cmd = ["ffprobe -show_streams {}".format(path)]
            p = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True
            )

            streams = []
            stream = {}

            for line in iter(p.stdout.readline, b''):
                line = line.decode('UTF-8', 'ignore')
                line = line.replace("\n", "")
                line = line.strip()

                if "[STREAM]" not in line and "[/STREAM]" not in line:
                    stream[line.split("=")[0]] = line.split("=")[1]

                if "[/STREAM]" in line:
                    streams.append(stream)
                    stream = {}

            for stream in streams:

                index = stream["index"]
                audio = stream["codec_type"] == "audio"
                language = stream["TAG:language"] if "TAG:language" in stream \
                    else None

                if audio and language in ["eng"] and not audio_stream:
                    audio_stream = "0:{}".format(index)

                if audio and language in ["por"] and not audio_stream:
                    audio_stream = "0:{}".format(index)

            if not audio_stream:
                audio_stream = "0:1"

            output = "/app/import/{}.mp4".format(name)
            process = subprocess.Popen(
                "ffmpeg -i {} -codec copy -map {} -map {} {} -y".format(
                    path, video_stream, audio_stream, output),
                shell=True,
                stdout=subprocess.PIPE
            )
            process.wait()

            if process.returncode == 0:
                print("\n")
                print("Done ({} of {}), from".format(i, len(videos)), path)
                print("to", output)
                print("\n")

                try:
                    os.remove(path)
                except Exception as e:
                    pass

        subtitles = glob.glob('/app/convert/*.srt')

        for i, path in enumerate(subtitles):
            source = open(path, 'r')
            destination = path.replace(".srt", ".vtt")
            destination = destination.replace("/convert/", "/import/")
            destination = open(destination.replace(".srt", ".vtt"), 'w')

            destination.write("WEBVTT\n\n")

            lines = source.readlines()

            for l, line in enumerate(lines):
                line = line.strip()
                line = re.sub('<[^<]+?>', '', line)
                line = line.replace(",", ".")
                destination.write("{}\n".format(line))

            source.close()
            destination.close()

            print("Converted", path)

        # videos = glob.glob('/app/convert/*.mp4')
        # for video in videos:
        #     os.remove(video)

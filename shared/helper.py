import boto3
import magic
import os
import os
import pytz
import subprocess
import sys
import threading
import uuid

from PIL import Image
from botocore.exceptions import ClientError
from datetime import datetime
from datetime import timedelta
from django.conf import settings
from moviepy.editor import VideoFileClip


class ProgressPercentage(object):

    def __init__(self, filename):
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            sys.stdout.write(
                "\r%s  %s / %s  (%.2f%%)" % (
                    self._filename, self._seen_so_far, self._size,
                    percentage))
            sys.stdout.flush()


class Helper:

    def __init__(self):
        self.s3 = boto3.client(
            "s3",
            endpoint_url="https://{}".format(os.environ.get("S3_BUCKET_URL")),
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY")
        )
        self.bucket = os.environ.get("S3_BUCKET")
        self.base_url = "https://{}/{}".format(
            os.environ.get("S3_BUCKET_URL"),
            self.bucket
        )

    def get_now(self):
        return datetime.now(pytz.timezone("America/Sao_Paulo"))

    def get_file_path(self, instance, filename):
        ext = filename.split(".")[-1]
        filename = "%s.%s" % (uuid.uuid4(), ext)
        return os.path.join("/app/tmp", filename)

    def upload_file(self, path, delete=True):
        file_name = os.path.basename(path)
        ext = file_name.split(".")[-1]
        name = file_name.split(".")[0]

        if ext not in ["mp4", "m4v", "jpg", "jpeg", "png", "vtt", "webp",
                       "gif",
                       "MP4", "M4V", "JPG", "JPEG", "PNG", "VTT", "WEBP",
                       "GIF"]:

            output = "/app/tmp/{}.mp4".format(name)
            process = subprocess.Popen(
                "ffmpeg -i {} -codec copy -map 0 {}".format(path, output),
                shell=True,
                stdout=subprocess.PIPE
            )
            process.wait()

            if process.returncode == 0:
                os.remove(path)
                path = output
                file_name = os.path.basename(path)
            else:
                if delete:
                    os.remove(path)
                return None

        try:
            mime = magic.Magic(mime=True)
            mime = mime.from_file(path)
            response = self.s3.upload_file(
                path,
                self.bucket,
                file_name,
                ExtraArgs={'ContentType': mime},
                Callback=ProgressPercentage(path)
            )
            print(response)
            if delete:
                os.remove(path)
            return file_name
        except Exception as e:
            print(e)
            return None

        return None

    def delete_file(self, obj):
        self.s3.delete_object(Bucket=self.bucket, Key=obj)

    def create_presigned_url(self, object, expiration=60):
        if not object:
            return None

        return "{}{}".format(self.base_url, object)

    def extract_frame(self, movie, frame):
        clip = VideoFileClip(movie)
        name = "{}.png".format(uuid.uuid4())
        imgpath = "/app/tmp/{}".format(name)
        clip.save_frame(imgpath, frame)
        return name

    def crop_image(self, image, x, y, w, h):
        input_image = Image.open(image)
        box = (x, y, x + w, y + h)
        output_image = input_image.crop(box)
        output_image.save(image)
        return image

    def resize_image(self, image, w, crop=0):
        # try:
        #     input_image = Image.open(image)
        #     percent = (w/float(input_image.size[0]))
        #     height = int((float(input_image.size[1])*float(percent)))
        #     resized_image = input_image.resize(
        #         (w, height),
        #         Image.Resampling.LANCZOS
        #     )
        #     resized_image.save(image)

        #     if crop > 0 and crop < height:
        #         y = (height - crop) / 2
        #         cropped = self.crop_image(image, 0, y, w, crop)
        #         return cropped
        # except Exception as e:
        #     print(e)

        return image

    def hide(self, user, query):
        if not user.groups.filter(name='special').exists():
            query = query.filter(hidden=False)
        return query

    def should_hide(self, user):
        if user.groups.filter(name='special').exists():
            return False
        return True

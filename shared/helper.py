import boto3
import json
import magic
import os
import pytz
import re
import requests
import subprocess
import sys
import threading
import uuid
import hashlib

from urllib.parse import urlencode
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

        # subtitle service
        self.osurl = "https://api.opensubtitles.com/api/v1"
        self.oskey = os.environ.get("OPENSUBTITLES_KEY")
        self.osuser = os.environ.get("OPENSUBTITLES_USER")
        self.ospass = os.environ.get("OPENSUBTITLES_PASS")

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

    def levenshtein_distance(self, s1, s2):
        m, n = len(s1), len(s2)

        # Initialize a matrix of size (m+1) x (n+1)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        # Initialize the first row and column
        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j

        # Compute the distances
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                cost = 0 if s1[i - 1] == s2[j - 1] else 1
                dp[i][j] = min(dp[i - 1][j] + 1,      # Deletion
                               dp[i][j - 1] + 1,      # Insertion
                               dp[i - 1][j - 1] + cost)  # Substitution

        return dp[m][n]

    def clean_movie_name(self, title):
        title = title.lower()
        title = title.replace(" ", "+")
        return title

    def get_subtitle(self, movie, language):

        try:
            data = {
                "languages": "pt-br",
                "query": self.clean_movie_name(movie.title),
                "type": "movie",
                "year": movie.date.year,
            }

            data = requests.get(
                url="{}/subtitles".format(self.osurl),
                params=data,
                headers={
                    "Content-Type": "application/json",
                    "Api-Key": self.oskey,
                    "User-Agent": "johnflix v1",
                },
            )

            data = data.json()["data"]

            for m in data:
                title = m["attributes"]["feature_details"]["title"]
                year = m["attributes"]["feature_details"]["year"]

                distance = self.levenshtein_distance(
                    "{} {}".format(movie.title, movie.date.year),
                    "{} {}".format(title, year)
                )

                if distance < 2:
                    if len(m["attributes"]["files"]) > 0:
                        file_id = m["attributes"]["files"][0]["file_id"]
                    return file_id
        except Exception as e:
            pass

        return None

    def download_subtitle(self, file_id):

        try:
            token = requests.post(
                url="{}/login".format(self.osurl),
                headers={
                    "Content-Type": "application/json",
                    "Api-Key": self.oskey,
                    "User-Agent": "johnflix v1",
                },
                data=json.dumps({
                    "username": self.osuser,
                    "password": self.ospass
                })
            ).json()["token"]

            file = requests.post(
                url="{}/download".format(self.osurl),
                headers={
                    "Content-Type": "application/json",
                    "Api-Key": self.oskey,
                    "User-Agent": "johnflix v1",
                    "Authorization": "Bearer {}".format(token),
                    "Accept": "application/json",
                },
                data=json.dumps({
                    "file_id": file_id
                })
            ).json()

            return file["link"]
        except Exception as e:
            pass

        return None

    def parse_subtitle(self, url):
        try:
            response = requests.get(url)
            name = str(uuid.uuid1())
            path = "/app/convert/{}.srt".format(name)

            with open(path, mode="wb") as file:
                file.write(response.content)

            source = open(path, 'r')
            destination = path.replace(".srt", ".vtt")
            destination = destination.replace("/convert/", "/tmp/")
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

            os.remove(path)

            final_path = self.upload_file("/app/tmp/{}.vtt".format(name))
            print(final_path)

            return "{}.vtt".format(name)
        except Exception as e:
            pass

        return None

    def get_cache_key(self, request):
        # Obtém o token do header Authorization
        token = request.headers.get('Authorization', '')

        # Obtém a URL base e os parâmetros GET em ordem alfabética
        url_path = request.path  # Somente a URL sem os parâmetros
        query_params = request.GET.dict()  # Obtém os parâmetros GET como dicionário
        sorted_query = urlencode(sorted(query_params.items()))  # Ordena os parâmetros GET

        # Concatena o token, o caminho e os parâmetros ordenados para gerar a chave
        key_data = "{}|{}|{}".format(token, url_path, sorted_query)

        # Cria um hash SHA-256 para garantir que a chave tenha um tamanho fixo
        cache_key = hashlib.sha256(key_data.encode()).hexdigest()
        return "cache_{}".format(cache_key)








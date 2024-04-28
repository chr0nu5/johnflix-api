import glob
import json
import os
import re
import subprocess

from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def __init__(self):
        super().__init__()
        self.extensions = ['mp4', 'm4v']

    def handle(self, *args, **options):

        videos = glob.glob('/app/convert/*')

        for path in videos:

            file_name = os.path.basename(path)
            ext = file_name.split(".")[-1]
            name = file_name.replace("." + ext, "")

            if ext in self.extensions:

                tags = re.findall(r'\((.*?)\)', name)
                genres = re.findall(r'\{(.*?)\}', name)

                title = name
                for t in tags:
                    title = title.replace("(" + t + ")", "")

                for g in genres:
                    title = title.replace("{" + g + "}", "")

                title = title.strip()
                title = re.sub(r'\s+', ' ', title)

                print("")
                print("Processing {} {} {}".format(title, tags, genres))
                print("")
                data = [
                    {
                        "title": title,
                        "date": None,
                        "tags": tags,
                        "genres": genres,
                        "file_path": "/app/import/{}.{}".format(name, ext),
                        "cover_path": None,
                        "subtitle_path": None,
                        "type": "movie",
                        "hidden": True
                    }]

                with open('/app/import/import_{}.json'.format(name), 'w') as f:
                    json.dump(data, f)

                os.rename(
                    "/app/convert/{}.{}".format(name, ext),
                    "/app/import/{}.{}".format(name, ext)
                )

                print("Saved {}".format(data))

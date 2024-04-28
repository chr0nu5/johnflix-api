import glob
import json
import mutagen
import os
import shutil
import uuid

from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def __init__(self):
        super().__init__()

    def handle(self, *args, **options):
        for file in glob.glob(
            "/app/convert/*.m*",
            recursive=True
        ):
            print("Starting {}".format(file))
            info = [{
                "title": "Movie",
                "date": None,
                "tags": [],
                "genres": [],
                "file_path": None,
                "cover_path": None,
                "subtitle_path": None,
                "type": "movie",
                "hidden": False
            }]
            data = mutagen.File(file)

            full_name = os.path.basename(file)
            name = os.path.basename(file)[:-4]

            if "©nam" in data and len(data["©nam"]) > 0:
                info[0]["title"] = data["©nam"][0]

            if "©day" in data and len(data["©day"]) > 0:
                info[0]["date"] = data["©day"][0]

            if "©gen" in data and len(data["©gen"]) > 0:
                info[0]["genres"] = [
                    g.strip().title() for g in data["©gen"][0].split(",")
                ]

            if "covr" in data and len(data["covr"]) > 0:
                cover = data["covr"][0]
                img = str(uuid.uuid1())
                with open("/app/import/{}.png".format(img), "wb") as image:
                    image.write(cover)
                info[0]["cover_path"] = "/app/import/" + img + ".png"

            info[0]["file_path"] = "/app/import/" + full_name

            with open(
                "/app/import/import_{}.json".format(name),
                "w"
            ) as metadata:
                metadata.write(json.dumps(info, indent=4))
                print("Generated import_{}.json".format(name))

            shutil.move(file, file.replace("convert", "import"))

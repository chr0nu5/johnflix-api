import glob
import json
import os
import random
import uuid

from content.models import Episode
from content.models import Genre
from content.models import Movie
from content.models import Photo
from content.models import PhotoCollection
from content.models import Season
from content.models import Subtitle
from content.models import Tag
from django import db
from django.core.management.base import BaseCommand
from moviepy.editor import VideoFileClip
from shared.cache import CacheManager
from shared.helper import Helper


class Command(BaseCommand):

    def __init__(self):
        super().__init__()
        self.helper = Helper()
        self.cache_manager = CacheManager()

    def sv_fl(self, file, delete=True, cover=False):

        original_file = file

        try:
            ext = file.split(".")[-1]
            new_name = str(uuid.uuid1())
            os.rename(file, "/app/import/{}.{}".format(new_name, ext))

            file = "/app/import/{}.{}".format(new_name, ext)

            clip = VideoFileClip(file)

            duration = clip.duration
            frames = clip.fps
            width, height = clip.size

            frame = int(clip.duration - (clip.duration/4))

            _cover = None

            if cover:
                _cover = self.helper.upload_file(cover)
            else:
                _cover = self.helper.extract_frame(file, frame)
                _cover = self.helper.upload_file("/app/tmp/{}".format(_cover))

            media = self.helper.upload_file(file, delete=delete)

            if not _cover or not media:
                print("\n")
                print("Retrying save {}".format(original_file))
                return self.sv_fl(original_file, delete=delete)

            return duration, frames, width, height, _cover, media
        except Exception as e:
            print(e)
            print("\n", "Error uploading {}, retrying".format(file))
        return self.sv_fl(file, delete=delete)

    def sv_ep_db(self, season, number, title, duration, frames, width, height,
                 date, cover, media, hidden, subtitle):
        episode = None
        try:
            season = Season.objects.get(pk=season)
            episode = Episode()
            episode.season = season
            episode.number = number
            episode.title = title
            episode.duration = duration
            episode.frames = frames
            episode.width = width
            episode.height = height
            episode.date = date
            episode.cover = cover
            episode.media = media
            episode.hidden = hidden
            episode.hidden = season.hidden
            if subtitle:
                episode.subtitle = subtitle
            episode.save()
            return episode
        except Exception as e:
            print("\n")
            print(e)
            print("\n")
            print("Error saving {}, retry".format(title))
            db.close_old_connections()
            return self.sv_ep_db(season,
                                 number,
                                 title,
                                 duration,
                                 frames,
                                 width,
                                 height,
                                 date,
                                 cover,
                                 media,
                                 subtitle)
        return episode

    def sv_tag_db(self, name, hidden):
        tag = None
        tag, created = Tag.objects.get_or_create(name=name, hidden=hidden)
        if not tag:
            return self.sv_tag_db(name)
        if created:
            print("\nSaved tag {}\n".format(tag.name))
        return tag

    def sv_genre_db(self, name, hidden):
        genre = None
        genre, created = Genre.objects.get_or_create(name=name, hidden=hidden)
        if not genre:
            return self.sv_tag_db(name)
        if created:
            print("\nSaved genre {}\n".format(genre.name))
        return genre

    def sv_mv_db(self, title, genres, tags, duration, frames, width, height,
                 date, cover, media, hidden, subtitle):
        movie = None
        try:
            movie = Movie()
            movie.title = title
            movie.duration = duration
            movie.frames = frames
            movie.width = width
            movie.height = height
            movie.date = date
            movie.cover = cover
            movie.media = media
            movie.hidden = hidden
            if subtitle:
                movie.subtitle = subtitle
            movie.save()

            for tag in tags:
                tag = self.sv_tag_db(tag, hidden)
                movie.tag.add(tag)

            for genre in genres:
                genre = self.sv_genre_db(genre, hidden)
                movie.genre.add(genre)

            return movie
        except Exception as e:
            print("\n")
            print(e)
            print("\n")
            print("Error saving {}, retry".format(title))
            db.close_old_connections()
            return self.sv_mv_db(title, genres, tags, duration, frames, width,
                                 height, date, cover, media, hidden, subtitle)
        return movie

    def sv_vtt_file(self, file, delete=True):
        ext = file.split(".")[-1]
        new_name = str(uuid.uuid1())
        os.rename(file, "/app/import/{}.{}".format(new_name, ext))
        file = "/app/import/{}.{}".format(new_name, ext)
        try:
            return self.helper.upload_file(file, delete=delete)
        except Exception as e:
            print("\n")
            print("Retrying save {}".format(file))
            return self.sv_vtt_file(file, delete=delete)

    def sv_vtt_db(self, file):
        try:
            subtitle = Subtitle()
            subtitle.language = "en"
            subtitle.label = "English"
            subtitle.vtt = file
            subtitle.save()
            return subtitle
        except Exception as e:
            print("\n")
            print(e)
            print("\n")
            print("Error saving {}, retry".format(file))
            db.close_old_connections()
            return sv_vtt_db(file)

    def sv_cl_db(
            self, collection_id, title, tags, genres, cover, hidden, delete
    ):
        collection = None
        try:
            if collection_id:
                collection = PhotoCollection.objects.filter(
                    id=collection_id
                ).first()
            if not collection:
                collection = PhotoCollection()

            collection.title = title
            collection.hidden = hidden
            collection.save()
        except Exception as e:
            print("\n")
            print(e)
            print("\n")
            print("Error saving {}, retry".format(title))
            db.close_old_connections()
            return self.sv_cl_db(
                collection_id, title, tags, genres, hidden, delete
            )
        return collection

    def sv_ph_db(self, collection, file, hidden, delete):
        try:

            ext = file.split(".")[-1]
            new_name = str(uuid.uuid1())
            os.rename(file, "/app/import/{}.{}".format(new_name, ext))
            file = "/app/import/{}.{}".format(new_name, ext)

            photo_file = self.helper.upload_file(file, delete=delete)
            photo = Photo()
            photo.photo = photo_file
            photo.hidden = hidden
            photo.save()
            collection.photos.add(photo)

            if not collection.cover:
                collection.cover = photo.photo.url
                collection.save()

            return photo
        except Exception as e:
            print("\n")
            print(e)
            print("\n")
            print("Error saving {}, retry".format(file))
            db.close_old_connections()
            return self.sv_ph_db(collection, file, hidden, delete)

    def handle(self, *args, **options):

        json_files = glob.glob('/app/import/import_*.json')
        if len(json_files) < 1:
            print(
                "No files to import. Make sure your files",
                "start with import_ and are .json files"
            )
        for json_file in json_files:

            data = open(json_file)
            data = json.load(data)

            if isinstance(data, list):
                print(
                    "Importing {} files from {}".format(
                        len(data),
                        json_file
                    )
                )

                for counter, item in enumerate(data):

                    type = item["type"]
                    file = item["file_path"]
                    date = item["date"]
                    title = item["title"]
                    title = title.replace(".", " ")
                    title = title.replace("-", " ")
                    title = title.title()
                    tags = item["tags"] if "tags" in item else []
                    subtitle = item[
                        "subtitle_path"] if "subtitle_path" in item else None
                    duration = 0
                    frames = 0
                    width = 0
                    height = 0
                    cover = None
                    media = None
                    hidden = item["hidden"]

                    if "cover_path" in item:
                        cover = item["cover_path"]

                    print("\n", "Started {} {}".format(type, file))

                    if subtitle:
                        subtitle = self.sv_vtt_file(subtitle)
                        subtitle = self.sv_vtt_db(subtitle)
                        print("\nUsing subtitle", subtitle.vtt)

                    duration, frames, width, height, cover, media = self.sv_fl(
                        file,
                        delete=False,
                        cover=cover if cover else False
                    )
                    print("\n", duration, frames, width, height, cover, media)

                    if type == "episode":
                        season = item["season_id"]
                        number = item["number"]
                        if cover and media:
                            item = self.sv_ep_db(
                                season, number, title, duration, frames, width,
                                height, date, cover, media, hidden, subtitle
                            )
                            if item:
                                print(
                                    "Done saving {} {}".format(file, item.id)
                                )
                                print("{} of {}".format(counter+1, len(data)))
                            else:
                                print("Error retrying saving {}".format(title))
                        else:
                            print("\n",
                                  "Error with cover and media for {}".format(
                                      file)
                                  )

                    if type == "movie":
                        genres = item["genres"]

                        if cover and media:
                            item = self.sv_mv_db(
                                title, genres, tags, duration,
                                frames, width, height, date,
                                cover, media, hidden,
                                subtitle
                            )
                            if item:
                                print(
                                    "Done saving {} {}".format(file, item.id)
                                )
                                print(
                                    "{} of {}".format(counter+1, len(data))
                                )
                            else:
                                print("Error retrying saving {}".format(title))
                        else:
                            print("\n",
                                  "Error with cover and media for {}".format(
                                      file)
                                  )

                    try:
                        os.remove("/app/import/{}".format(media))
                    except Exception as e:
                        print(e)

                    files = glob.glob('/app/tmp/*')
                    for file in files:
                        if file not in ["/app/tmp/.keep", "/app/tmp/done"]:
                            os.remove(file)

                print("\n")
                print(
                    "Finished importing {} files from {}".format(
                        len(data),
                        json_file
                    )
                )
                os.remove(json_file)
            else:
                print(
                    "Importing {} photos from {}".format(
                        len(data["files"]),
                        json_file
                    )
                )

                collection_id = data["collection_id"]
                title = data["title"]
                tags = data["tags"]
                genres = data["genres"]
                files = data["files"]
                hidden = data["hidden"]
                cover = random.choice(files)

                collection = self.sv_cl_db(
                    collection_id, title, tags, genres, cover, hidden, False
                )

                for i, file in enumerate(files):
                    photo = self.sv_ph_db(collection, file, hidden, True)
                    print("\n\nSaved photo {} of {}, {}".format(
                        i, len(files), file)
                    )

                print(
                    "\nFinished importing {} photos from {}".format(
                        len(files),
                        json_file
                    )
                )
                os.remove(json_file)

                files = glob.glob('/app/tmp/*')
                for file in files:
                    if file not in ["/app/tmp/.keep", "/app/tmp/done"]:
                        os.remove(file)

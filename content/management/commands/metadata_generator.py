import glob
import json
import mutagen
import os
import requests
import shutil
import sys
import time
import uuid

from content.models import Movie
from content.models import Tag
from django.core.management.base import BaseCommand


def query_number(question, default=1):
    valid = [1, 2, 3, 4, 5]
    prompt = " [1, 2, 3, 4, 5] "

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if int(choice) in valid:
            return int(choice) - 1
        else:
            sys.stdout.write(
                "Please respond with 1, 2, 3, 4 or 5 ")


def query_yes_no(question, default="yes"):
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == "":
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write(
                "Please respond with 'yes' or 'no' " "(or 'y' or 'n')")


class Command(BaseCommand):

    def __init__(self):
        super().__init__()
        self.key = "66525ca337f3dc982c8497ea07caba09"
        self.api_url = "https://api.themoviedb.org"
        self.img_url = "https://image.tmdb.org"

    def handle(self, *args, **options):

        movies_done = Movie.objects.filter(
            metadata=True,
            hidden=False,
        ).exclude(bypass_metadata=True).count()

        movies_to_do = Movie.objects.filter(
            metadata=False,
            hidden=False,
        ).exclude(bypass_metadata=True).count()

        print()
        print("Welcome, you have done {} movies, we have {} to do.".format(
            movies_done, movies_to_do
        ))

        movies = Movie.objects.filter(
            metadata=False,
            hidden=False,
            bypass_metadata=False
        ).order_by("-id")

        print()
        print("Working with {} movie(s)".format(len(movies)))
        print()

        time.sleep(5)

        for movie in movies:

            os.system('cls' if os.name == 'nt' else 'clear')

            print("{} - {} (search)".format(movie.title, movie.date))
            print()

            response = requests.get(
                url="{}/3/search/movie".format(self.api_url),
                params={
                    "query": movie.title,
                    "language": "en-US",
                    "api_key": self.key,
                },
            ).json()

            movie_data = None
            cast_data = None
            _index = None

            if "results" in response and len(response["results"]) > 0:
                for i, _result in enumerate(response["results"][:5]):
                    print(
                        "({}) - {} - {}".format(
                            i+1,
                            _result["title"],
                            _result["release_date"]
                        )
                    )
                    print(_result["overview"])
                    print()
            else:
                movie.bypass_metadata = True
                movie.save()
                print()
                print("No data found, looping")
                print("{} updated".format(movie.title))
                time.sleep(2)
                continue

            if movie.title.lower() == response["results"][0][
                "original_title"].lower() and \
                    str(movie.date) == str(
                        response["results"][0]["release_date"]
            ):
                print("Item 1 is perfect, processing")
                print()
                _index = 0
            else:
                _index = query_number("Type the index")
                print()

            movie_data = response["results"][_index]

            if movie_data:
                response = requests.get(
                    url="{}/3/movie/{}/credits".format(
                        self.api_url,
                        movie_data["id"]
                    ),
                    params={
                        "language": "en-US",
                        "api_key": self.key,
                    },
                ).json()

                if "cast" in response and len(response["cast"]) > 0:
                    cast_data = response["cast"][:3]
                    for cast in cast_data:
                        print(cast["name"])
                    print()

                _confirm = False
                if movie.title.lower() == movie_data[
                    "original_title"].lower() and \
                        str(movie.date) == str(movie_data["release_date"]):
                    _confirm = True
                    print("Item is perfect, processing")
                    print()
                else:
                    print(
                        "({}) - {} - {}".format(
                            _index + 1,
                            movie_data["title"],
                            movie_data["release_date"]
                        )
                    )
                    print(movie_data["overview"])
                    print()

                    _confirm = query_yes_no("Is this ok?")

                if _confirm:
                    movie.title = movie_data["original_title"]
                    if not movie.description:
                        movie.description = movie_data["overview"]
                    if not movie.date:
                        movie.date = movie_data["release_date"]
                    movie.save()
                else:
                    movie.bypass_metadata = True
                    movie.save()

                if cast_data and _confirm:
                    for cast in cast_data:
                        _tag, created = Tag.objects.get_or_create(
                            name=cast["name"]
                        )
                        if created:
                            print()
                            print("Created tag {}".format(cast["name"]))
                        else:
                            print()
                            print("Using tag {}".format(cast["name"]))

                        if not _tag.cover:
                            response = requests.get(
                                url="{}/t/p/w780{}".format(
                                    self.img_url,
                                    cast["profile_path"]
                                ),
                                params={
                                    "language": "en-US",
                                    "api_key": self.key,
                                },
                                stream=True
                            )

                            _img = "/app/tmp{}".format(cast["profile_path"])
                            if response.status_code == 200:
                                with open(
                                    _img,
                                    "wb"
                                ) as out_file:
                                    shutil.copyfileobj(
                                        response.raw,
                                        out_file
                                    )
                            else:
                                _img = None

                            if _img:
                                _tag.cover = _img.replace("/app/tmp", "tmp")
                                _tag.save()
                                print()

                        movie.tag.add(_tag)

                if _confirm:
                    movie.metadata = True
                    movie.save()
                    print()
                    print()
                    print("{} updated".format(movie.title))

                    time.sleep(2)

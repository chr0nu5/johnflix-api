import json
import random
import re
import time

from content.models import Content
from content.models import Episode
from content.models import Genre
from content.models import Media
from content.models import MessageWatchParty
from content.models import Movie
from content.models import Photo
from content.models import PhotoCollection
from content.models import Playlist
from content.models import Progress
from content.models import Season
from content.models import Subtitle
from content.models import Tag
from content.models import WatchList
from content.models import WatchParty
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.postgres.search import SearchVector
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework.authtoken.models import Token
from shared.helper import Helper
from shared.token import AuthToken
from shared.token import authorization

helper = Helper()


class ProgressView(View):

    @method_decorator(authorization)
    def get(self, request):

        watching = {"episodes": [], "movies": []}

        progresses = Progress.objects.filter(
            user=request.user,
            episode__isnull=False
        ).order_by("-modified_date")[:4]

        for progress in progresses:

            season = "S0{}".format(
                progress.episode.season.number
                if progress.episode.season.number < 10 else "S{}".format(
                    progress.episode.season.number
                )
            )
            epi = "E{}".format(
                "0{}".format(progress.episode.number)
                if progress.episode.number < 10 else "{}".format(
                    progress.episode.number)
            )

            watching["episodes"].append({
                "time": progress.time,
                "volume": progress.volume,
                "speed": progress.speed,
                "duration": progress.episode.duration,
                "path": "episode",
                "hash": progress.episode.hash,
                "title": "{}: {}{}".format(
                    progress.episode.season.media.name, season, epi
                ),
                "subtitle": progress.episode.title,
                "image": helper.create_presigned_url(
                    progress.episode.cover.url if progress.episode.cover else
                    None, expiration=progress.episode.duration * 2
                ),
                "watchlist": progress.episode.is_watchlist(
                    request.user,
                    WatchList
                )
            })

        # if not request.user.is_superuser:
        #     return JsonResponse(watching, safe=False, status=200)

        hidden = request.GET.get("hidden", 0)
        if not request.user.is_superuser:
            hidden = 0

        progresses = Progress.objects.filter(
            user=request.user,
            movie__isnull=False,
            movie__hidden=hidden
        ).order_by("-modified_date")[:4]

        for progress in progresses:

            tag = progress.movie.tag.all().filter(hidden=True).first()
            if tag:
                tag = tag.name + ", "
            else:
                tag = ""
            genre = progress.movie.genre.all().filter(hidden=True).first()
            if genre:
                genre = genre.name
            else:
                genre = ""

            watching["movies"].append({
                "time": progress.time,
                "volume": progress.volume,
                "speed": progress.speed,
                "duration": progress.movie.duration,
                "path": "movie",
                "hash": progress.movie.hash,
                "subtitle":
                    progress.movie.date.year if progress.movie.date else
                    "{}{}".format(tag, genre),
                "title": progress.movie.title,
                "image": helper.create_presigned_url(
                    progress.movie.cover.url if progress.movie.cover else None,
                    expiration=progress.movie.duration * 2),
                "watchlist": progress.movie.is_watchlist(
                    request.user,
                    WatchList)
            })

        return JsonResponse(watching, safe=False, status=200)

    @method_decorator(authorization)
    def put(self, request, hash):

        progress = None

        episode = Episode.objects.filter(hash=hash).first()
        if episode:
            progress, created = Progress.objects.get_or_create(
                user=request.user,
                episode=episode)
        else:
            movie = Movie.objects.filter(hash=hash).first()
            if movie:
                progress, created = Progress.objects.get_or_create(
                    user=request.user,
                    movie=movie)

        if not progress:
            return JsonResponse({
                "error": "Media not found"
            }, safe=False, status=400)

        end = request.GET.get("end", None)
        if end != "null":
            #     progress.delete()
            return JsonResponse({
                "success": True,
                "deleted": True
            }, safe=False, status=200)

        time = request.GET.get("time", None)
        volume = request.GET.get("volume", None)
        speed = request.GET.get("speed", None)

        progress.time = time
        progress.volume = volume
        progress.speed = speed
        progress.save()

        # if progress.episode:
        #     episodes = Progress.objects.filter(
        #         episode__season__media=progress.episode.season.media,
        #     ).exclude(pk=progress.pk).delete()

        return JsonResponse({
            "success": True,
            "deleted": False
        }, safe=False, status=200)


class ContentView(View):

    @method_decorator(authorization)
    def get(self, request, hash=None):

        if hash:
            content = Content.objects.filter(hash=hash).first()
            if not content:
                return JsonResponse({
                    "error": "Content not found"
                }, safe=False, status=400)

            data = []

            medias = Media.objects.filter(
                content=content,
            ).order_by("-id")

            if not request.user.is_superuser:
                medias = medias.filter(hidden=False)

            return JsonResponse({
                "hash": content.hash,
                "path": "content",
                "title": content.name,
                "image": helper.create_presigned_url(
                    content.cover.url if content.cover else None,
                    expiration=settings.CACHE_TTL
                ),
                "medias": [{
                    "hash": media.hash,
                    "path": "media",
                    "title": media.name,
                    "image": helper.create_presigned_url(
                        media.cover.url if media.cover else None,
                        expiration=settings.CACHE_TTL
                    )
                } for media in medias]
            }, safe=False, status=200)

        all_contents = Content.objects.all().order_by("name")

        contents = []

        contents.append({
            "hash": "",
            "path": "movies",
            "title": "Movies",
            "image": "https://s3.us-west-004.backblazeb2.com/johnflix/movies."
            "jpeg"
        })

        contents.append({
            "hash": "",
            "path": "movies/genres",
            "title": "Genres",
            "image": "https://s3.us-west-004.backblazeb2.com/johnflix/movies."
            "jpeg"
        })

        contents.append({
            "hash": "",
            "path": "movies/tags",
            "title": "Tags",
            "image": "https://s3.us-west-004.backblazeb2.com/johnflix/movies."
            "jpeg"
        })

        for c in all_contents:
            contents.append({
                "hash": c.hash,
                "path": "content",
                "title": c.name,
                "image": helper.create_presigned_url(
                    c.cover.url if c.cover else None,
                    expiration=settings.CACHE_TTL
                )
            })

        if request.user.is_superuser:
            contents.append({
                "hash": "",
                "path": "hidden",
                "title": "Hidden",
                "image": "https://s3.us-west-004.backblazeb2.com/johnflix/"
                "hidden"
            })

            contents.append({
                "hash": "",
                "path": "hidden/genres",
                "title": "(H) Genres",
                "image": "https://s3.us-west-004.backblazeb2.com/johnflix/"
                "hidden"
            })

            contents.append({
                "hash": "",
                "path": "hidden/tags",
                "title": "(H) Tags",
                "image": "https://s3.us-west-004.backblazeb2.com/johnflix/"
                "hidden"
            })

            contents.append({
                "hash": "",
                "path": "photos",
                "title": "Photos",
                "image": "https://s3.us-west-004.backblazeb2.com/johnflix/"
                "photos.jpg"
            })

        return JsonResponse(contents, safe=False, status=200)


class MediaView(View):

    @method_decorator(authorization)
    def get(self, request, hash=None):

        media = Media.objects.filter(hash=hash).first()
        if not media:
            return JsonResponse({
                "error": "Media not found"
            }, safe=False, status=400)

        content = {
            "hash": media.hash,
            "title": media.name,
            "path": "media",
            "back": {
                    "path": "content",
                    "hash": media.content.hash
            },
            "image": helper.create_presigned_url(
                media.cover.url if media.cover else None,
                expiration=settings.CACHE_TTL
            ),
            "seasons": []
        }
        seasons = Season.objects.filter(
            media=media,
        ).order_by("number")

        if not request.user.is_superuser:
            seasons = seasons.filter(hidden=False)

        for season in seasons:
            episodes = Episode.objects.filter(
                season=season,
            ).order_by("number")

            if not request.user.is_superuser:
                episodes = episodes.filter(hidden=False)
            episodes = episodes[:5]

            content["seasons"].append({
                "title": "Season {}".format(season.number),
                "hash": season.hash,
                "path": "season",
                "image": helper.create_presigned_url(
                    media.cover.url if media.cover else None,
                    expiration=settings.CACHE_TTL
                ),
                "episodes": [{
                    "number": episode.number,
                    "title": episode.title,
                    "hash": episode.hash,
                    "path": "episode",
                    "duration": "{}mins".format(
                        int(episode.duration/60)
                    ) if episode.duration else 0,
                    "image": helper.create_presigned_url(
                        episode.cover.url if episode.cover else None,
                        expiration=settings.CACHE_TTL
                    )} for episode in episodes]
            })

        return JsonResponse(content, safe=False, status=200)


class SeasonView(View):

    @method_decorator(authorization)
    def get(self, request, hash=None):

        season = Season.objects.filter(hash=hash).first()
        if not season:
            return JsonResponse({
                "error": "Sason not found"
            }, safe=False, status=400)

        episodes = Episode.objects.filter(
            season=season,
        ).order_by("number")

        if not request.user.is_superuser:
            episodes = episodes.filter(hidden=False)

        subtitle = "Season {}".format(season.number)

        if season.title:
            subtitle = "Season {} - {}".format(season.number, season.title)

        data = []
        for episode in episodes:

            progress = Progress.objects.filter(
                user=request.user,
                episode=episode
            ).first()

            data.append({
                "time": progress.time if progress else None,
                "duration": episode.duration,
                "number": episode.number,
                "title": episode.title,
                "hash": episode.hash,
                "path": "episode",
                "subtitle": ("{}mins".format(
                        int(episode.duration/60)
                ) if episode.duration else 0) + ", {} view(s)".format(
                    episode.views),
                "image": helper.create_presigned_url(
                    episode.cover.url if episode.cover else None,
                    expiration=settings.CACHE_TTL
                ),
                "watchlist": episode.is_watchlist(
                    request.user,
                    WatchList
                )})

        content = {
            "title": season.media.name,
            "hash": season.hash,
            "subtitle": subtitle,
            "path": "season",
            "back": {
                "path": "media",
                "hash": season.media.hash
            },
            "image": helper.create_presigned_url(
                season.media.cover.url if season.media.cover else None,
                expiration=settings.CACHE_TTL
            ),
            "episodes": data
        }

        return JsonResponse(content, safe=False, status=200)


class GenreView(View):

    @method_decorator(authorization)
    def get(self, request, hash=None):

        if hash:
            genre = Genre.objects.filter(hash=hash).first()
            if not genre:
                return JsonResponse({
                    "error": "Genre not found"
                }, safe=False, status=400)

            items = []

            media_b = Movie.objects.filter(
                genre__in=[genre]
            ).order_by("-id").only(
                "id",
                "title",
                "hash",
                "cover",
                "description"
            )
            if not request.user.is_superuser:
                media_b = media_b.filter(hidden=False)

            paginator = Paginator(media_b, 40)

            page = int(request.GET.get("page", "1"))

            if page < 1:
                page = 1
            if page > paginator.num_pages:
                page = paginator.num_pages

            page = paginator.page(page)

            for media in page.object_list:
                items.append({
                    "title": media.title,
                    "hash": media.hash,
                    "subtitle": None,
                    "path": "movie",
                    "image": helper.create_presigned_url(
                        media.cover.url if media.cover else None,
                        expiration=settings.CACHE_TTL
                    ),
                    "watchlist": media.is_watchlist(
                        request.user,
                        WatchList
                    )
                })

            data = {
                "title": genre.name,
                "hash": genre.hash,
                "subtitle": None,
                "path": "genre",
                "image": helper.create_presigned_url(
                    genre.cover.url if genre.cover else None,
                    expiration=settings.CACHE_TTL
                ),
                "items": items,
                "total_pages": paginator.num_pages
            }

            return JsonResponse(data, safe=False, status=200)

        hidden = request.GET.get("hidden", 0)
        if not request.user.is_superuser:
            hidden = 0

        genres = Genre.objects.filter(hidden=hidden).order_by("order",
                                                              "name")

        items = []

        for genre in genres:
            _items = []
            for media in Movie.objects.filter(
                genre__in=[genre], hidden=False
            ).order_by("?")[:8]:
                _items.append({
                    "title": media.title if hasattr(
                        media,
                        "title"
                    ) else media.name,
                    "hash": media.hash,
                    "subtitle": None,
                    "path": "movie",
                    "image": helper.create_presigned_url(
                        media.cover.url if media.cover else None,
                        expiration=settings.CACHE_TTL
                    ),
                    "watchlist": media.is_watchlist(
                        request.user,
                        WatchList
                    )
                })
            items.append({
                "title": genre.name,
                "hash": genre.hash,
                "path": "genre",
                "featured": genre.featured,
                "order": genre.order,
                "description": genre.description,
                "items": _items,
                "image": helper.create_presigned_url(
                    genre.cover.url if genre.cover else None,
                    expiration=settings.CACHE_TTL
                )
            })

        return JsonResponse(items, safe=False, status=200)


class TagView(View):

    @method_decorator(authorization)
    def get(self, request, hash=None):

        if hash:
            tag = Tag.objects.filter(hash=hash).first()
            if not tag:
                return JsonResponse({
                    "error": "Tag not found"
                }, safe=False, status=400)

            items = []

            # media_a = Episode.objects.filter(
            #     tag__in=[tag]
            # ).order_by("-id").only("id", "title", "hash", "cover")
            # if not request.user.is_superuser:
            #     media_a = media_a.filter(hidden=False)

            media_b = Movie.objects.filter(
                tag__in=[tag]
            ).order_by("-id").only(
                "id",
                "title",
                "hash",
                "cover",
                "description"
            )
            if not request.user.is_superuser:
                media_b = media_b.filter(hidden=False)

            # paginator = Paginator(media_a.union(media_b, all=True), 40)
            paginator = Paginator(media_b, 40)

            page = int(request.GET.get("page", "1"))

            if page < 1:
                page = 1
            if page > paginator.num_pages:
                page = paginator.num_pages

            page = paginator.page(page)

            for media in page.object_list:

                items.append({
                    "title": media.title if hasattr(
                        media,
                        "title"
                    ) else media.name,
                    "hash": media.hash,
                    "subtitle": None,
                    "description": media.description,
                    "path": "movie",
                    "image": helper.create_presigned_url(
                        media.cover.url if media.cover else None,
                        expiration=settings.CACHE_TTL
                    ),
                    "watchlist": media.is_watchlist(
                        request.user,
                        WatchList
                    )
                })

            data = {
                "title": tag.name,
                "hash": tag.hash,
                "path": "tag",
                "image": helper.create_presigned_url(
                    tag.cover.url if tag.cover else None,
                    expiration=settings.CACHE_TTL
                ),
                "items": items,
                "total_pages": paginator.num_pages
            }

            return JsonResponse(data, safe=False, status=200)

        hidden = request.GET.get("hidden", 0)
        if not request.user.is_superuser:
            hidden = 0
        tags = Tag.objects.filter(hidden=hidden).order_by("order", "name")

        return JsonResponse([{
            "title": tag.name,
            "hash": tag.hash,
            "path": "tag",
            "order": tag.order,
            "image": helper.create_presigned_url(
                tag.cover.url if tag.cover else None,
                expiration=settings.CACHE_TTL
            )
        } for tag in tags], safe=False, status=200)


class EpisodeView(View):

    @method_decorator(authorization)
    def get(self, request, hash=None):

        curr_ep = Episode.objects.filter(hash=hash).first()
        if not curr_ep:
            return JsonResponse({
                "error": "Episode not found"
            }, safe=False, status=400)

        previous_ep = helper.hide(
            request.user, Episode.objects).filter(
            season=curr_ep.season,
            number=curr_ep.number-1,
        ).order_by("number").first()
        next_ep = helper.hide(
            request.user, Episode.objects).filter(
            season=curr_ep.season,
            number=curr_ep.number+1,
        ).order_by("number").first()

        if not previous_ep:
            previous_ep = helper.hide(
                request.user, Episode.objects).filter(
                season=curr_ep.season,
                number=curr_ep.number-2,
            ).order_by("number").first()

        if not next_ep:
            next_ep = helper.hide(
                request.user, Episode.objects).filter(
                season=curr_ep.season,
                number=curr_ep.number+2,
            ).order_by("number").first()

        if not previous_ep:
            season = helper.hide(
                request.user, Season.objects).filter(
                media=curr_ep.season.media,
                number=curr_ep.season.number-1,
            ).first()
            if season:
                previous_ep = helper.hide(
                    request.user, Episode.objects).filter(
                    season=season,
                ).order_by("number").last()

        if not next_ep:
            season = helper.hide(
                request.user, Season.objects).filter(
                media=curr_ep.season.media,
                number=curr_ep.season.number+1,
            ).first()
            if season:
                next_ep = helper.hide(
                    request.user, Episode.objects).filter(
                    season=season,
                ).order_by("number").first()

        curr_ep.views = curr_ep.views + 1
        curr_ep.save()

        season = "S0{}".format(
            curr_ep.season.number if curr_ep.season.number < 10 else
            "S{}".format(
                curr_ep.season.number
            )
        )
        ep = "E{}".format(
            "0{}".format(curr_ep.number) if curr_ep.number < 10 else
            "{}".format(
                curr_ep.number)
        )

        progress = Progress.objects.filter(
            user=request.user,
            episode=curr_ep
        ).first()

        subtitle = curr_ep.subtitle
        if subtitle:
            subtitle = {
                "language": subtitle.language,
                "label": subtitle.label,
                "vtt": helper.create_presigned_url(
                    subtitle.vtt.url if subtitle.vtt else None,
                    expiration=curr_ep.duration * 2
                )
            }

        data = {
            "progress": {
                "time": progress.time,
                "volume": progress.volume,
                "speed": progress.speed,
            } if progress else None,
            "season": "{}{}".format(season, ep),
            "title": curr_ep.title,
            "hash": curr_ep.hash,
            "date": curr_ep.date,
            "views": curr_ep.views,
            "duration": curr_ep.duration,
            "width": curr_ep.width,
            "height": curr_ep.height,
            "subtitle": subtitle,
            "media": helper.create_presigned_url(
                curr_ep.media.url if curr_ep.media else None,
                expiration=curr_ep.duration * 2
            ),
            "image": helper.create_presigned_url(
                curr_ep.cover.url if curr_ep.cover else None,
                expiration=curr_ep.duration * 2
            ),
            "watchlist": curr_ep.is_watchlist(
                request.user,
                WatchList
            ),
            "description": curr_ep.description if curr_ep.description else "",
            "all": "/season/{}/".format(curr_ep.season.hash),
            "path": "episode",
            "next": {
                "hash": next_ep.hash,
                "name": next_ep.title,
                "path": "episode",
                "image": helper.create_presigned_url(
                    next_ep.cover.url if next_ep.cover else None,
                    expiration=next_ep.duration * 2
                )
            } if next_ep else None,
            "previous": {
                "hash": previous_ep.hash,
                "name": previous_ep.title,
                "path": "episode",
                "image": helper.create_presigned_url(
                    previous_ep.cover.url if previous_ep.cover else None,
                    expiration=previous_ep.duration * 2
                )
            } if previous_ep else None,
            "tags": [{
                "name": tag.name,
                "hash": tag.hash,
                "image": helper.create_presigned_url(
                    tag.cover.url if tag.cover else None,
                    expiration=settings.CACHE_TTL
                ),
            } for tag in helper.hide(
                request.user, curr_ep.tag.all())],
            "genres": [{
                "name": genre.name,
                "hash": genre.hash,
                "image": helper.create_presigned_url(
                    genre.cover.url if genre.cover else None,
                    expiration=settings.CACHE_TTL
                ),
            } for genre in helper.hide(
                request.user, curr_ep.season.media.genre.all())]
        }

        for p in Progress.objects.filter(
            user=request.user,
            episode__isnull=False
        ).order_by("-modified_date")[4:]:
            p.delete()

        return JsonResponse(data)


class AllMoviesView(View):

    @method_decorator(authorization)
    def get(self, request, hash=None):

        order = request.GET.get("order", "-id")

        if order not in ["id", "-id", "date", "title", "-date", "-title"]:
            order = "-id"

        hidden = request.GET.get("hidden", 0)
        if not request.user.is_superuser:
            hidden = 0

        movies = Movie.objects.filter(hidden=hidden).order_by(order)

        paginator = Paginator(movies, 40)

        page = int(request.GET.get("page", "1"))

        if page < 1:
            page = 1
        if page > paginator.num_pages:
            page = paginator.num_pages

        page = paginator.page(page)

        data = []

        for movie in page.object_list:
            progress = Progress.objects.filter(
                user=request.user,
                movie=movie
            ).first()
            data.append({
                "time": progress.time if progress else None,
                "duration": movie.duration,
                "title": movie.title,
                "subtitle": movie.date.year if movie.date else str(
                    movie.tag.all().first() if
                    movie.tag.all().first() else ""
                ) + " " + str(
                    movie.genre.all().first() if
                    movie.genre.all().first() else ""
                ),
                "hash": movie.hash,
                "path": "movie",
                "image": helper.create_presigned_url(
                    movie.cover.url if movie.cover else None,
                    expiration=settings.CACHE_TTL
                ),
                "watchlist": movie.is_watchlist(request.user, WatchList)
            })

        return JsonResponse({
            "total_pages": paginator.num_pages,
            "items": data
        }, safe=False)


class MovieView(View):

    @method_decorator(authorization)
    def get(self, request, hash=None):

        curr_ep = Movie.objects.filter(hash=hash).first()
        if not curr_ep:
            return JsonResponse({
                "error": "Movie not found"
            }, safe=False, status=400)

        if not request.user.is_superuser and curr_ep.hidden:
            return JsonResponse({
                "error": "Forbidden"
            }, safe=False, status=403)

        in_playlist = Playlist.objects.filter(movies=curr_ep).first()

        previous_ep = None
        next_ep = None

        if in_playlist and len(in_playlist.movies.all()) > 2:
            movies = in_playlist.movies.all().order_by("date")
            all_movies = []
            for m in movies:
                all_movies.append(m)

            curr_index = None
            for i, m in enumerate(all_movies):
                if m.pk == curr_ep.pk:
                    curr_index = i

            if curr_index == 0:
                previous_ep = all_movies[len(all_movies)-1]
                next_ep = all_movies[curr_index + 1]
            if curr_index == len(all_movies) - 1:
                previous_ep = all_movies[curr_index-1]
                next_ep = all_movies[0]

            if not previous_ep:
                previous_ep = all_movies[curr_index - 1]
            if not next_ep:
                next_ep = all_movies[curr_index + 1]

        else:
            previous_ep = Movie.objects.filter(
                tag__in=[curr_ep.tag.all().order_by("?").first()]
            ).order_by("?").first()
            next_ep = Movie.objects.filter(
                tag__in=[curr_ep.tag.all().order_by("?").first()]
            ).order_by("?").first()

        curr_ep.views = curr_ep.views + 1
        curr_ep.save()

        progress = Progress.objects.filter(
            user=request.user,
            movie=curr_ep
        ).first()

        subtitle = curr_ep.subtitle
        if subtitle:
            subtitle = {
                "language": subtitle.language,
                "label": subtitle.label,
                "vtt": helper.create_presigned_url(
                    subtitle.vtt.url if subtitle.vtt else None,
                    expiration=curr_ep.duration * 2
                )
            }

        embed = None
        if curr_ep.embed:
            try:
                embed = re.findall(r'(https?://\S+)', curr_ep.embed)[0]
            except Exception as e:
                pass

        data = {
            "progress": {
                "time": progress.time,
                "volume": progress.volume,
                "speed": progress.speed,
            } if progress else None,
            "season": None,
            "title": curr_ep.title,
            "hash": curr_ep.hash,
            "date": curr_ep.date,
            "views": curr_ep.views,
            "duration": curr_ep.duration,
            "width": curr_ep.width,
            "height": curr_ep.height,
            "description": curr_ep.description,
            "embed": embed,
            "subtitle": subtitle,
            "media": helper.create_presigned_url(
                curr_ep.media.url if curr_ep.media else None,
                expiration=curr_ep.duration * 2
            ),
            "image": helper.create_presigned_url(
                curr_ep.cover.url if curr_ep.cover else None,
                expiration=curr_ep.duration * 2
            ),
            "watchlist": curr_ep.is_watchlist(
                request.user,
                WatchList
            ),
            "description": curr_ep.description if curr_ep.description else "",
            "all": "/movies/",
            "path": "movie",
            "next": {
                "hash": next_ep.hash,
                "name": next_ep.title,
                "path": "movie",
                "image": helper.create_presigned_url(
                    next_ep.cover.url if next_ep.cover else None,
                    expiration=next_ep.duration * 2
                )
            } if next_ep else None,
            "previous": {
                "hash": previous_ep.hash,
                "name": previous_ep.title,
                "path": "movie",
                "image": helper.create_presigned_url(
                    previous_ep.cover.url if previous_ep.cover else None,
                    expiration=previous_ep.duration * 2
                )
            } if previous_ep else None,
            "tags": [{
                "name": tag.name,
                "hash": tag.hash,
                "image": helper.create_presigned_url(
                    tag.cover.url if tag.cover else None,
                    expiration=settings.CACHE_TTL
                ),
            } for tag in helper.hide(
                request.user, curr_ep.tag.all())],
            "genres": [{
                "name": genre.name,
                "hash": genre.hash,
                "image": helper.create_presigned_url(
                    genre.cover.url if genre.cover else None,
                    expiration=settings.CACHE_TTL
                ),
            } for genre in helper.hide(
                request.user, curr_ep.genre.all())]
        }

        for p in Progress.objects.filter(
            user=request.user,
            movie__isnull=False
        ).order_by("-modified_date")[4:]:
            p.delete()

        return JsonResponse(data)


class PhotoView(View):

    @method_decorator(authorization)
    def get(self, request, hash=None):

        if not request.user.is_superuser:
            return JsonResponse({
                "error": "Forbidden"
            }, safe=False, status=403)

        if hash:
            collection = PhotoCollection.objects.filter(hash=hash).first()
            if not collection:
                return JsonResponse({
                    "error": "Collection not found"
                }, safe=False, status=400)

            photos = collection.photos.all().order_by("-id")

            paginator = Paginator(photos, 40)

            page = int(request.GET.get("page", "1"))

            if page < 1:
                page = 1
            if page > paginator.num_pages:
                page = paginator.num_pages

            page = paginator.page(page)

            data = []

            for photo in page.object_list:
                data.append({
                    "hash": photo.id,
                    "image": helper.create_presigned_url(
                        photo.photo.url if photo.photo else None,
                        expiration=settings.CACHE_TTL
                    )
                })

            return JsonResponse({
                "title": collection.title,
                "hash": collection.hash,
                "path": "photos",
                "items": data,
                "total_pages": paginator.num_pages
            }, safe=False)

        collections = PhotoCollection.objects.all().order_by("title")

        data = [
            {
                "title": collection.title,
                "hash": collection.hash,
                "path": "photo",
                "image": helper.create_presigned_url(
                    collection.cover.url if collection.cover else None,
                    expiration=settings.CACHE_TTL
                )
            } for collection in collections
        ]

        return JsonResponse(data, safe=False)


class RandomView(View):

    @method_decorator(authorization)
    def get(self, request, type=None):

        if type == "movies":
            hidden = request.GET.get("hidden", 0)
            if not request.user.is_superuser:
                hidden = 0

            movies = Movie.objects.filter(hidden=hidden).order_by("?")[:8]
            data = []

            for movie in movies:
                progress = Progress.objects.filter(
                    user=request.user,
                    movie=movie
                ).first()

                data.append({
                    "time": progress.time if progress else None,
                    "duration": movie.duration,
                    "title": movie.title,
                    "subtitle": movie.date.year if movie.date else None,
                    "hash": movie.hash,
                    "path": "movie",
                    "image": helper.create_presigned_url(
                        movie.cover.url if movie.cover else None,
                        expiration=settings.CACHE_TTL
                    ),
                    "watchlist": movie.is_watchlist(
                        request.user,
                        WatchList
                    )
                })

            return JsonResponse(data, safe=False)

        if type == "episodes":
            episodes = Episode.objects.all()
            if not request.user.is_superuser:
                episodes = episodes.filter(hidden=False)
            episodes = episodes.order_by("?")[:8]

            data = []
            for episode in episodes:
                progress = Progress.objects.filter(
                    user=request.user,
                    episode=episode
                ).first()
                data.append({
                    "time": progress.time if progress else None,
                    "duration": episode.duration,
                    "subtitle": episode.title,
                    "hash": episode.hash,
                    "title": episode.season.media.name,
                    "path": "episode",
                    "image": helper.create_presigned_url(
                        episode.cover.url if episode.cover else None,
                        expiration=settings.CACHE_TTL
                    ),
                    "watchlist": episode.is_watchlist(
                        request.user,
                        WatchList
                    )
                })
            return JsonResponse(data, safe=False)

        return JsonResponse([], safe=False)


class LatestView(View):

    @method_decorator(authorization)
    def get(self, request, type=None):

        if type == "movies":
            hidden = request.GET.get("hidden", 0)
            if not request.user.is_superuser:
                hidden = 0

            movies = Movie.objects.filter(hidden=hidden).order_by("-id")

            movies = movies[:8]

            data = []

            for movie in movies:

                tag = movie.tag.all().filter(hidden=True).first()
                if tag:
                    tag = tag.name + ", "
                else:
                    tag = ""
                genre = movie.genre.all().filter(hidden=True).first()
                if genre:
                    genre = genre.name
                else:
                    genre = ""

                progress = Progress.objects.filter(user=request.user,
                                                   movie=movie).first()

                data.append({
                    "time": progress.time if progress else None,
                    "duration": movie.duration,
                    "title": movie.title,
                    "subtitle": movie.date.year if movie.date else
                    "{}{}".format(tag, genre),
                    "hash": movie.hash,
                    "path": "movie",
                    "image": helper.create_presigned_url(
                        movie.cover.url if movie.cover else None,
                        expiration=settings.CACHE_TTL
                    ),
                    "watchlist": movie.is_watchlist(
                        request.user,
                        WatchList
                    )
                })

            return JsonResponse(data, safe=False)

        if type == "episodes":
            episodes = Episode.objects.all()
            if not request.user.is_superuser:
                episodes = episodes.filter(hidden=False)
            episodes = episodes.order_by("-id")[:8]

            data = []
            for episode in episodes:
                progress = Progress.objects.filter(user=request.user,
                                                   episode=episode).first()
                data.append({
                    "time": progress.time if progress else None,
                    "duration": episode.duration,
                    "subtitle": episode.title,
                    "hash": episode.hash,
                    "title": episode.season.media.name,
                    "path": "episode",
                    "image": helper.create_presigned_url(
                        episode.cover.url if episode.cover else None,
                        expiration=settings.CACHE_TTL
                    ),
                    "watchlist": episode.is_watchlist(
                        request.user,
                        WatchList
                    )
                })

            return JsonResponse(data, safe=False)

        return JsonResponse([], safe=False)


class SearchView(View):

    @method_decorator(authorization)
    def get(self, request):

        items = []

        s = request.GET.get("s", "")

        if s == "undefined":
            s = ""

        t = request.GET.get("t", "").split(",")
        g = request.GET.get("g", "").split(",")

        if len(s) < 3 and len(t) < 1 and len(g) < 1:
            return JsonResponse({
                "error": "At least 3 letters, a tag and/or a genre is required"
            }, safe=False, status=400)

        episodes = Episode.objects.annotate(
            search=SearchVector("title") + SearchVector("subtitle"),
        ).filter(search=s, hidden=False).order_by("-id")

        episodes = episodes[:64]

        for episode in episodes:

            season = "S0{}".format(
                episode.season.number
                if episode.season.number < 10 else "S{}".format(
                    episode.season.number
                )
            )
            epi = "E{}".format(
                "0{}".format(episode.number)
                if episode.number < 10 else "{}".format(
                    episode.number)
            )

            progress = Progress.objects.filter(user=request.user,
                                               episode=episode).first()

            items.append({
                "time": progress.time if progress else None,
                "duration": episode.duration,
                "title": episode.title,
                "hash": episode.hash,
                "subtitle": "{}, {}{}".format(
                    episode.season.media.name,
                    season,
                    epi
                ),
                "path": "episode",
                "image": helper.create_presigned_url(
                    episode.cover.url if episode.cover else None,
                    expiration=settings.CACHE_TTL
                ),
                "watchlist": episode.is_watchlist(
                    request.user,
                    WatchList
                )
            })

        _movies = Movie.objects.all()

        for genre in g:
            genre = Genre.objects.filter(hash=genre).first()
            if genre:
                _movies = _movies.filter(genre=genre)

        for tag in t:
            tag = Tag.objects.filter(hash=tag).first()
            if tag:
                _movies = _movies.filter(tag=tag)

        if len(s) > 3:
            _movies = _movies.annotate(
                search=SearchVector(
                    "title") + SearchVector(
                    "subtitle"),
            ).filter(search=s, hidden=False).order_by("?")

        movies = _movies.order_by("?")[:40]

        _added = []

        for movie in movies:

            if movie.hash in _added:
                continue

            progress = Progress.objects.filter(user=request.user,
                                               movie=movie).first()
            items.append({
                "time": progress.time if progress else None,
                "duration": movie.duration,
                "title": movie.title,
                "subtitle": None,
                "hash": movie.hash,
                "path": "movie",
                "image": helper.create_presigned_url(
                    movie.cover.url if movie.cover else None,
                    expiration=settings.CACHE_TTL
                ),
                "watchlist": movie.is_watchlist(
                    request.user,
                    WatchList
                )
            })
            _added.append(movie.hash)

        return JsonResponse({
            "s": s,
            "items": items
        }, safe=False, status=200)


class RecommendedView(View):

    @method_decorator(authorization)
    def get(self, request):

        items = []
        hash = request.GET.get("hash", None)

        if len(hash) < 36:
            return JsonResponse({
                "items": []
            }, safe=False, status=200)

        _movie = Movie.objects.filter(hash=hash).first()
        if not _movie:
            return JsonResponse({
                "hash": hash,
                "items": []
            }, safe=False, status=200)

        _tags = _movie.tag.all()
        _genres = _movie.genre.all()
        _movies = Movie.objects

        _s = " ".join(
            [
                word if len(word) >
                2 else "" for word in _movie.title.split(" ")
            ]
        )

        _added = []

        if len(_s) > 3:
            _movies = _movies.annotate(
                search=SearchVector(
                    "title") + SearchVector(
                    "subtitle") + SearchVector(
                    "description"),
            ).filter(search=_s)

        _movies = _movies.filter(hidden=_movie.hidden).order_by("?")

        for movie in _movies:
            progress = Progress.objects.filter(user=request.user,
                                               movie=movie).first()
            if _movie.hash != movie.hash and movie.hash not in _added:
                items.append({
                    "time": progress.time if progress else None,
                    "duration": movie.duration,
                    "title": movie.title,
                    "subtitle": None,
                    "hash": movie.hash,
                    "path": "movie",
                    "image": helper.create_presigned_url(
                        movie.cover.url if movie.cover else None,
                        expiration=settings.CACHE_TTL
                    ),
                    "watchlist": movie.is_watchlist(
                        request.user,
                        WatchList
                    )
                })
                _added.append(movie.hash)

        if len(items) < 8:
            _movies = Movie.objects.filter(tag__in=_tags)
            _movies = _movies.filter(hidden=_movie.hidden).order_by("?")
            _movies = _movies[:8]

            for movie in _movies:
                progress = Progress.objects.filter(user=request.user,
                                                   movie=movie).first()
                if _movie.hash != movie.hash and movie.hash not in _added:
                    items.append({
                        "time": progress.time if progress else None,
                        "duration": movie.duration,
                        "title": movie.title,
                        "subtitle": None,
                        "hash": movie.hash,
                        "path": "movie",
                        "image": helper.create_presigned_url(
                            movie.cover.url if movie.cover else None,
                            expiration=settings.CACHE_TTL
                        ),
                        "watchlist": movie.is_watchlist(
                            request.user,
                            WatchList
                        )
                    })
                    _added.append(movie.hash)

        if len(items) < 8:
            _movies = Movie.objects.filter(genre__in=_genres)
            _movies = _movies.filter(hidden=_movie.hidden).order_by("?")
            _movies = _movies[:8]
            for movie in _movies:
                progress = Progress.objects.filter(user=request.user,
                                                   movie=movie).first()
                if _movie.hash != movie.hash and movie.hash not in _added:
                    items.append({
                        "time": progress.time if progress else None,
                        "duration": movie.duration,
                        "title": movie.title,
                        "subtitle": None,
                        "hash": movie.hash,
                        "path": "movie",
                        "image": helper.create_presigned_url(
                            movie.cover.url if movie.cover else None,
                            expiration=settings.CACHE_TTL
                        ),
                        "watchlist": movie.is_watchlist(
                            request.user,
                            WatchList
                        )
                    })
                    _added.append(movie.hash)

        return JsonResponse({
            "items": items[:8]
        }, safe=False, status=200)


class UserView(View):

    @method_decorator(authorization)
    def get(self, request):

        return JsonResponse({
            "username": request.user.username,
            "is_superuser": request.user.is_superuser
        }, safe=False, status=200)


class AuthView(View):

    def post(self, request):

        data = request.body
        try:
            data = json.loads(data)
        except Exception as e:
            return JsonResponse({
                "error": "Invalid data"
            }, safe=False, status=400)

        username = data.get("username", None)
        password = data.get("password", None)

        if not username or not password:
            return JsonResponse({
                "error": "Missing username and/or password"
            }, safe=False, status=400)

        _user = authenticate(username=username, password=password)
        if not _user:
            return JsonResponse({
                "error": "Invalid username or password"
            }, safe=False, status=400)

        user = User.objects.filter(username=username).first()
        if not user:
            return JsonResponse({
                "error": "User not found"
            }, safe=False, status=400)

        token = AuthToken()
        _token = token.get_token(_user)

        return JsonResponse({
            "token": _token
        }, safe=False, status=200)


class WathListView(View):

    @method_decorator(authorization)
    def get(self, request):

        items = WatchList.objects.filter(user=request.user)

        paginator = Paginator(items, 40)

        page = int(request.GET.get("page", "1"))

        if page < 1:
            page = 1
        if page > paginator.num_pages:
            page = paginator.num_pages

        page = paginator.page(page)

        data = []

        for item in page.object_list:
            progress = None
            _type = None

            if item.episode:
                progress = Progress.objects.filter(
                    user=request.user,
                    episode=item.episode
                ).first()
                item = item.episode
                _type = "episode"
            elif item.movie:
                progress = Progress.objects.filter(
                    user=request.user,
                    movie=item.movie
                ).first()
                item = item.movie
                _type = "movie"

            data.append({
                "time": progress.time if progress else None,
                "duration": item.duration,
                "title": item.title,
                "subtitle": None,
                "hash": item.hash,
                "path": _type,
                "image": helper.create_presigned_url(
                    item.cover.url if item.cover else None,
                    expiration=settings.CACHE_TTL
                ),
                "watchlist": True
            })

        return JsonResponse({
            "total_pages": paginator.num_pages,
            "items": data
        }, safe=False)

    @method_decorator(authorization)
    def post(self, request):

        data = request.body
        try:
            data = json.loads(data)
        except Exception as e:
            return JsonResponse({
                "error": "Invalid data"
            }, safe=False, status=400)

        episode = data.get("episode", None)
        movie = data.get("movie", None)

        if episode:
            episode = Episode.objects.filter(hash=episode).first()
            if episode:
                watchlist, created = WatchList.objects.get_or_create(
                    episode=episode,
                    user=request.user
                )
                if not created:
                    watchlist.delete()
                return JsonResponse({
                    "watchlist": created
                }, safe=False, status=200)

        if movie:
            movie = Movie.objects.filter(hash=movie).first()
            if movie:
                watchlist, created = WatchList.objects.get_or_create(
                    movie=movie,
                    user=request.user
                )
                if not created:
                    watchlist.delete()
                return JsonResponse({
                    "watchlist": created
                }, safe=False, status=200)

        return JsonResponse({
            "error": "Missing episode or movie"
        }, safe=False, status=400)


class WatchPartyView(View):

    @method_decorator(authorization)
    def post(self, request):

        data = request.body
        try:
            data = json.loads(data)
        except Exception as e:
            return JsonResponse({
                "error": "Invalid data"
            }, safe=False, status=400)

        movie = data.get("movie", None)
        movie = Movie.objects.filter(hash=movie).first()
        if not movie:
            return JsonResponse({
                "error": "Movie not found"
            }, safe=False, status=400)

        watch_party = WatchParty()
        watch_party.user = request.user
        watch_party.movie = movie
        watch_party.save()

        return JsonResponse({
            "hash": watch_party.hash
        }, safe=False, status=200)

    @method_decorator(authorization)
    def get(self, request, hash=None, id=0):

        watch_party = WatchParty.objects.filter(hash=hash).first()
        if not watch_party:
            return JsonResponse({
                "error": "Watch Party not found"
            }, safe=False, status=400)

        chat = []

        messages = MessageWatchParty.objects.filter(
            watch_party=watch_party,
            pk__gt=id
        )

        for message in messages:
            chat.append({
                "id": message.pk,
                "user": message.user.username,
                "text": message.text,
                "timestamp": message.created_date,
                "self": request.user.pk == message.user.pk
            })

        return JsonResponse({
            "hash": watch_party.hash,
            "playing": watch_party.playing,
            "current_time": watch_party.current_time,
            "movie": {
                "title": watch_party.movie.title,
                "hash": watch_party.movie.hash
            },
            "messages": chat
        }, safe=False, status=200)

    @method_decorator(authorization)
    def patch(self, request, hash=None):

        data = request.body
        try:
            data = json.loads(data)
        except Exception as e:
            return JsonResponse({
                "error": "Invalid data"
            }, safe=False, status=400)

        text = data.get("text", None)
        if not text:
            return JsonResponse({
                "error": "Invalid text"
            }, safe=False, status=400)

        watch_party = WatchParty.objects.filter(hash=hash).first()
        if not watch_party:
            return JsonResponse({
                "error": "Watch Party not found"
            }, safe=False, status=400)

        message = MessageWatchParty()
        message.user = request.user
        message.text = text
        message.watch_party = watch_party
        message.save()

        return JsonResponse({}, safe=False, status=200)


class PlaylistView(View):

    @method_decorator(authorization)
    def get(self, request, hash=None):

        if hash:
            playlist = Playlist.objects.filter(hash=hash).first()
            if not playlist:
                return JsonResponse({
                    "error": "Playlist not found"
                }, safe=False, status=400)

            items = []
            for media in playlist.movies.all().order_by("date"):
                items.append({
                    "title": media.title,
                    "hash": media.hash,
                    "subtitle": media.date.year if media.date else None,
                    "path": "movie",
                    "image": helper.create_presigned_url(
                        media.cover.url if media.cover else None,
                        expiration=settings.CACHE_TTL
                    ),
                    "watchlist": media.is_watchlist(
                        request.user,
                        WatchList
                    )
                })

            data = {
                "title": playlist.name,
                "hash": playlist.hash,
                "subtitle": None,
                "path": "playlist",
                "image": helper.create_presigned_url(
                    playlist.cover.url if playlist.cover else None,
                    expiration=settings.CACHE_TTL
                ),
                "items": items
            }

            return JsonResponse(data, safe=False, status=200)

        hidden = request.GET.get("hidden", 0)
        if not request.user.is_superuser:
            hidden = 0

        playlists = Playlist.objects.filter(hidden=hidden)

        items = []

        for playlist in playlists:
            _items = []
            for media in playlist.movies.all().order_by("date"):
                _items.append({
                    "title": media.title if hasattr(
                        media,
                        "title"
                    ) else media.name,
                    "hash": media.hash,
                    "subtitle": media.date.year if media.date else None,
                    "path": "movie",
                    "image": helper.create_presigned_url(
                        media.cover.url if media.cover else None,
                        expiration=settings.CACHE_TTL
                    ),
                    "watchlist": media.is_watchlist(
                        request.user,
                        WatchList
                    )
                })
            items.append({
                "title": playlist.name,
                "hash": playlist.hash,
                "path": "playlist",
                "items": _items,
                "image": helper.create_presigned_url(
                    playlist.cover.url if playlist.cover else None,
                    expiration=settings.CACHE_TTL
                )
            })

        return JsonResponse(items, safe=False, status=200)


class SubtitleView(View):

    def get(self, request, hash, language):

        if language == "PT":
            language = "pt-br"

        if language not in ["pt-br"]:
            return JsonResponse({
                "error": "Invalid Language. [PT, EN]"
            }, safe=False, status=200)

        movie = Movie.objects.filter(hash=hash).first()
        if not movie:
            return JsonResponse({
                "error": "Movie not found"
            }, safe=False, status=400)

        if movie.subtitle and movie.subtitle.language in ["PT", "pt"]:
            return JsonResponse({
                "error": "Movie has subtitle"
            }, safe=False, status=400)

        file_id = helper.get_subtitle(movie, language)

        url = None
        if file_id:
            url = helper.download_subtitle(file_id)

        vtt = None
        if url:
            vtt = helper.parse_subtitle(url)

        if vtt:
            s = Subtitle()
            s.language = "PT"
            s.label = "Portuguese"
            s.vtt = vtt
            s.save()

            movie.subtitle = s
            movie.save()

        return JsonResponse({
            "movie": movie.title,
            "language": language
        }, safe=False, status=200)


class BlankView(View):

    def get(self, request):
        return JsonResponse({}, safe=False, status=200)

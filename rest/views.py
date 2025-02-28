from content.models import Content
from content.models import Episode
from content.models import Genre
from content.models import Media
from content.models import Movie
from content.models import Photo
from content.models import PhotoCollection
from content.models import Playlist
from content.models import Progress
from content.models import Season
from content.models import Subtitle
from content.models import Tag
from content.models import WatchList
from django.conf import settings
from django.contrib.postgres.search import SearchQuery
from django.contrib.postgres.search import SearchRank
from django.contrib.postgres.search import SearchVector
from django.db.models import Count
from django.db.models import F
from django.db.models import Prefetch
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest.middlewares import IsSuperUserOrVisibleOnly
from rest.mixins import CachedListMixin
from rest.mixins import HashFilterMixin
from rest.mixins import HiddenFilterMixin
from rest.mixins import OrderingMixin
from rest.pagination import CustomPageNumberPagination
from rest.serializers import ContentSerializer
from rest.serializers import EpisodeSerializer
from rest.serializers import GenreSerializer
from rest.serializers import MediaSerializer
from rest.serializers import MovieSerializer
from rest.serializers import PhotoCollectionSerializer
from rest.serializers import PhotoSerializer
from rest.serializers import PlaylistSerializer
from rest.serializers import SeasonSerializer
from rest.serializers import TagSerializer
from rest_framework import viewsets
from rest_framework.permissions import BasePermission
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from shared.helper import Helper

helper = Helper()


class IsSuperUserOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser


class GenericViewSet(HiddenFilterMixin,
                     OrderingMixin,
                     HashFilterMixin,
                     viewsets.ModelViewSet):
    pass


class GenreViewSet(CachedListMixin, GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAuthenticated, IsSuperUserOrVisibleOnly]
    filter_backends = [DjangoFilterBackend]
    pagination_class = CustomPageNumberPagination

    allowed_order_fields = {
        "created_date": "created_date",
        "name": "name"
    }

    def get_queryset(self):
        queryset = super(GenreViewSet, self).get_queryset()
        queryset = self.filter_hidden(queryset)
        queryset = self.filter_ordering(queryset)

        return queryset


class GenreMoviesViewSet(CachedListMixin, GenericViewSet):
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticated, IsSuperUserOrVisibleOnly]
    pagination_class = CustomPageNumberPagination

    allowed_order_fields = {
        "date": "date",
        "title": "title"
    }

    def get_queryset(self):
        genre_hash = self.kwargs.get("hash")
        queryset = Movie.objects.filter(genre__hash=genre_hash).distinct()
        queryset = self.filter_hidden(queryset)
        queryset = self.filter_ordering(queryset)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)

        genre_hash = self.kwargs.get("hash")
        genre = Genre.objects.filter(hash=genre_hash).first()

        if not genre:
            return Response({"error": "Genre not found."}, status=404)

        genre_data = GenreSerializer(genre).data

        return self.get_paginated_response({
            "info": genre_data,
            "movies": serializer.data
        })


class TagViewSet(CachedListMixin, GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated, IsSuperUserOrVisibleOnly]
    filter_backends = [DjangoFilterBackend]
    pagination_class = CustomPageNumberPagination

    allowed_order_fields = {
        "created_date": "created_date",
        "name": "name"
    }

    def get_queryset(self):
        queryset = super(TagViewSet, self).get_queryset()
        queryset = self.filter_hidden(queryset)
        queryset = self.filter_ordering(queryset)

        return queryset


class TagMoviesViewSet(CachedListMixin, GenericViewSet):
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticated, IsSuperUserOrVisibleOnly]
    pagination_class = CustomPageNumberPagination

    allowed_order_fields = {
        "date": "date",
        "title": "title"
    }

    def get_queryset(self):
        tag_hash = self.kwargs.get("hash")
        queryset = Movie.objects.filter(tag__hash=tag_hash).distinct()
        queryset = self.filter_hidden(queryset)
        queryset = self.filter_ordering(queryset)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)

        tag_hash = self.kwargs.get("hash")
        tag = Tag.objects.filter(hash=tag_hash).first()

        if not tag:
            return Response({"error": "Tag not found."}, status=404)

        tag_data = TagSerializer(tag).data

        return self.get_paginated_response({
            "info": tag_data,
            "movies": serializer.data
        })


class MovieViewSet(CachedListMixin, GenericViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticated, IsSuperUserOrVisibleOnly]
    filter_backends = [DjangoFilterBackend]
    pagination_class = CustomPageNumberPagination

    allowed_order_fields = {
        "date": "date",
        "title": "title",
        "created_date": "created_date"
    }

    def get_queryset(self):
        queryset = super(MovieViewSet, self).get_queryset()
        queryset = self.filter_hash(queryset)
        queryset = self.filter_hidden(queryset)
        queryset = self.filter_ordering(queryset)

        genre_ids = self.request.query_params.get("genre")
        if genre_ids:
            genre_ids = genre_ids.split(",")
            queryset = queryset.filter(genre__hash__in=genre_ids).distinct()

        tag_ids = self.request.query_params.get("tag")
        if tag_ids:
            tag_ids = tag_ids.split(",")
            queryset = queryset.filter(tag__hash__in=tag_ids).distinct()

        return queryset


class ContentViewSet(CachedListMixin, GenericViewSet):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    permission_classes = [IsAuthenticated, IsSuperUserOrVisibleOnly]
    filter_backends = [DjangoFilterBackend]
    pagination_class = CustomPageNumberPagination

    allowed_order_fields = {
        "date": "date",
        "name": "name"
    }

    def get_queryset(self):
        queryset = super(ContentViewSet, self).get_queryset()
        queryset = self.filter_hidden(queryset)
        queryset = self.filter_ordering(queryset)

        return queryset


class ContentMediasViewSet(CachedListMixin, GenericViewSet):
    serializer_class = MediaSerializer
    permission_classes = [IsAuthenticated, IsSuperUserOrVisibleOnly]
    pagination_class = CustomPageNumberPagination

    allowed_order_fields = {
        "date": "date",
        "name": "name"
    }

    def get_queryset(self):
        content_hash = self.kwargs.get("hash")
        queryset = Media.objects.filter(content__hash=content_hash)
        queryset = self.filter_hidden(queryset)
        queryset = self.filter_ordering(queryset)

        return queryset


class MediaSeasonsViewSet(CachedListMixin, GenericViewSet):
    serializer_class = SeasonSerializer
    permission_classes = [IsAuthenticated, IsSuperUserOrVisibleOnly]
    pagination_class = CustomPageNumberPagination

    allowed_order_fields = {
        "number": "number"
    }

    def get_queryset(self):
        media_hash = self.kwargs.get("hash")
        queryset = Season.objects.filter(media__hash=media_hash)
        queryset = self.filter_hidden(queryset)
        queryset = self.filter_ordering(queryset)
        return queryset


class SeasonEpisodesViewSet(CachedListMixin, GenericViewSet):
    serializer_class = EpisodeSerializer
    permission_classes = [IsAuthenticated, IsSuperUserOrVisibleOnly]
    pagination_class = CustomPageNumberPagination

    allowed_order_fields = {
        "number": "number"
    }

    def get_queryset(self):
        season_hash = self.kwargs.get("hash")
        queryset = Episode.objects.filter(season__hash=season_hash)
        queryset = self.filter_hidden(queryset)
        queryset = self.filter_ordering(queryset)
        return queryset


class EpisodeViewSet(CachedListMixin, GenericViewSet):
    queryset = Episode.objects.all()
    serializer_class = EpisodeSerializer
    permission_classes = [IsAuthenticated, IsSuperUserOrVisibleOnly]
    filter_backends = [DjangoFilterBackend]
    pagination_class = CustomPageNumberPagination

    allowed_order_fields = {
        "hash": "hash"
    }

    def get_queryset(self):
        queryset = super(EpisodeViewSet, self).get_queryset()
        queryset = self.filter_hash(queryset)

        return queryset


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        username = request.user.username
        menu = []

        # menu.append({"name": "Movies", "slug": "movies", "url": "movies"})
        menu.append({"name": "Genres", "slug": "genres", "url": "genres"})

        hidden_param = request.query_params.get("hidden")
        contents_qs = Content.objects.all()

        if request.user.is_superuser:
            if hidden_param is not None:
                if hidden_param.lower() == "true":
                    contents_qs = contents_qs.filter(hidden=True)
                    menu.append(
                        {"name": "Tags", "slug": "tags", "url": "tags"}
                    )
                elif hidden_param.lower() == "false":
                    contents_qs = contents_qs.filter(hidden=False)
        else:
            contents_qs = contents_qs.filter(hidden=False)

        for content in contents_qs.order_by("name"):
            menu.append({
                "hash": content.hash,
                "name": content.name,
                "url": "content/{}".format(content.hash)
            })

        if request.user.is_superuser and hidden_param and \
                hidden_param.lower() == "true":
            menu.append({"name": "Photos", "slug": "photos"})

        return Response({
            "username": username,
            "super": request.user.is_superuser,
            "menu": menu
        })


class UserWatchingView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination

    def get(self, request, format=None):
        user = request.user
        qs = Progress.objects.filter(user=user)

        hidden_param = request.query_params.get("hidden")

        if not user.is_superuser:
            qs = qs.filter(
                (Q(movie__isnull=False) & Q(movie__hidden=False)) |
                (Q(episode__isnull=False) & Q(episode__hidden=False))
            )
        else:
            if hidden_param is not None:
                if hidden_param.lower() == "true":
                    qs = qs.filter(
                        (Q(movie__isnull=False) & Q(movie__hidden=True)) |
                        (Q(episode__isnull=False) & Q(episode__hidden=True))
                    )
                elif hidden_param.lower() == "false":
                    qs = qs.filter(
                        (Q(movie__isnull=False) & Q(movie__hidden=False)) |
                        (Q(episode__isnull=False) & Q(episode__hidden=False))
                    )
        qs = qs.order_by("-created_date")

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(qs, request)

        results = []
        for progress in page:
            if progress.movie:
                data = MovieSerializer(
                    progress.movie,
                    context={
                        "request": request
                    }
                ).data
                data["type"] = "movie"
                results.append(data)
            elif progress.episode:
                data = EpisodeSerializer(
                    progress.episode,
                    context={
                        "request": request
                    }
                ).data
                data["type"] = "episode"
                results.append(data)

        return paginator.get_paginated_response(results)


class UserWatchlistView(APIView):
    permission_classes = [IsAuthenticated, IsSuperUserOrVisibleOnly]

    def get(self, request, format=None):
        user = request.user
        movies = Movie.objects.filter(watchlist__user=user).distinct()
        episodes = Episode.objects.filter(watchlist__user=user).distinct()

        hidden_param = request.query_params.get("hidden")

        if not user.is_superuser:
            movies = movies.filter(hidden=False)
            episodes = episodes.filter(hidden=False)
        else:
            if hidden_param is not None:
                if hidden_param.lower() == "true":
                    movies = movies.filter(hidden=True)
                    episodes = episodes.filter(hidden=True)
                elif hidden_param.lower() == "false":
                    movies = movies.filter(hidden=False)
                    episodes = episodes.filter(hidden=False)

        movie_paginator = CustomPageNumberPagination()
        episode_paginator = CustomPageNumberPagination()
        movie_page = movie_paginator.paginate_queryset(movies, request)
        episode_page = episode_paginator.paginate_queryset(episodes, request)

        movie_serializer = MovieSerializer(
            movie_page, many=True, context={"request": request})
        episode_serializer = EpisodeSerializer(
            episode_page, many=True, context={"request": request})

        movie_paginated = movie_paginator.get_paginated_response(
            movie_serializer.data).data
        episode_paginated = episode_paginator.get_paginated_response(
            episode_serializer.data).data

        return Response({
            "movies": movie_paginated,
            "episodes": episode_paginated
        })


class AddOrRemoveWatchListView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        hash_val = request.data.get("hash")
        if not hash_val:
            return Response({"error": "Hash is required"}, status=400)

        try:
            movie = Movie.objects.get(hash=hash_val)
            watchlist_entry = WatchList.objects.filter(
                user=request.user, movie=movie).first()
            if watchlist_entry:
                watchlist_entry.delete()
                return Response({
                    "message": "Movie removed from watchlist"
                }, status=200)
            else:
                WatchList.objects.create(user=request.user, movie=movie)
                return Response({
                    "message": "Movie added to watchlist"
                }, status=201)
        except Movie.DoesNotExist:
            try:
                episode = Episode.objects.get(hash=hash_val)
                watchlist_entry = WatchList.objects.filter(
                    user=request.user, episode=episode).first()
                if watchlist_entry:
                    watchlist_entry.delete()
                    return Response({
                        "message": "Episode removed from watchlist"
                    }, status=200)
                else:
                    WatchList.objects.create(
                        user=request.user, episode=episode)
                    return Response({
                        "message": "Episode added to watchlist"
                    }, status=201)
            except Episode.DoesNotExist:
                return Response({
                    "error": "No movie or episode found with that hash"
                }, status=404)


class GalleriesViewSet(CachedListMixin, GenericViewSet):
    queryset = PhotoCollection.objects.all()
    serializer_class = PhotoCollectionSerializer
    permission_classes = [IsAuthenticated, IsSuperUserOnly]
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        return self.queryset


class GalleryPhotosViewSet(CachedListMixin, GenericViewSet):
    serializer_class = PhotoSerializer
    permission_classes = [IsAuthenticated, IsSuperUserOnly]
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        gallery_hash = self.kwargs.get("hash")
        try:
            collection = PhotoCollection.objects.get(hash=gallery_hash)
        except PhotoCollection.DoesNotExist:
            from django.db.models import QuerySet
            return QuerySet().none()
        return collection.photos.all()


class ProgressSaveView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        item_hash = request.data.get("hash")
        time_value = request.data.get("time")
        if not item_hash or time_value is None:
            return Response({
                "error": "hash and time are required."
            }, status=400)

        movie = Movie.objects.filter(hash=item_hash).first()
        episode = None
        if not movie:
            episode = Episode.objects.filter(hash=item_hash).first()
            if not episode:
                return Response({"error": "Invalid hash."}, status=404)

        if movie:
            progress = Progress.objects.filter(
                user=request.user, movie=movie).first()
            if progress:
                progress.time = time_value
                progress.save()
            else:
                Progress.objects.create(
                    user=request.user, movie=movie, time=time_value)
        else:
            progress = Progress.objects.filter(
                user=request.user, episode=episode).first()
            if progress:
                progress.time = time_value
                progress.save()
            else:
                Progress.objects.create(
                    user=request.user, episode=episode, time=time_value)

        return Response({"status": "success"})


class SearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        s = request.GET.get("search", "")
        tags_param = request.GET.get("tag", "")
        genres_param = request.GET.get("genre", "")

        tags_list = [item for item in tags_param.split(
            ",") if item] if tags_param else []
        genres_list = [item for item in genres_param.split(
            ",") if item] if genres_param else []

        if len(s) < 3 and not tags_list and not genres_list:
            return Response({
                "error": "At least 3 letters, a tag and/or a genre is required"
            }, status=400)

        qs = Movie.objects.all()

        if not request.user.is_superuser:
            qs = qs.filter(hidden=False)
        else:
            hidden_param = request.GET.get("hidden")
            if hidden_param is not None:
                if hidden_param.lower() == "true":
                    qs = qs.filter(hidden=True)
                elif hidden_param.lower() == "false":
                    qs = qs.filter(hidden=False)
            else:
                qs = qs.filter(hidden=False)

        for genre_hash in genres_list:
            try:
                genre = Genre.objects.get(hash=genre_hash)
                qs = qs.filter(genre=genre)
            except Genre.DoesNotExist:
                continue

        for tag_hash in tags_list:
            try:
                tag = Tag.objects.get(hash=tag_hash)
                qs = qs.filter(tag=tag)
            except Tag.DoesNotExist:
                continue

        if s and len(s) >= 3:
            vector = SearchVector(
                "title",
                weight='A'
            ) + SearchVector(
                "subtitle",
                weight='B'
            ) + SearchVector(
                "description",
                weight='C'
            )
            query = SearchQuery(s)
            qs = qs.annotate(
                rank=SearchRank(vector, query)
            ).filter(
                rank__gte=0.1
            ).order_by("-rank")
        else:
            qs = qs.order_by("title")

        qs = qs[:settings.REST_FRAMEWORK["PAGE_SIZE"]]

        serializer = MovieSerializer(
            qs,
            many=True,
            context={"request": request}
        )
        data = {"results": serializer.data}

        return Response(data)


class PlaylistViewSet(CachedListMixin, GenericViewSet):
    queryset = Playlist.objects.prefetch_related(
        Prefetch('movies', queryset=Movie.objects.order_by('date'))
    )
    serializer_class = PlaylistSerializer
    permission_classes = [IsAuthenticated, IsSuperUserOrVisibleOnly]
    filter_backends = [DjangoFilterBackend]
    pagination_class = CustomPageNumberPagination

    allowed_order_fields = {
        "created_date": "created_date",
        "name": "name"
    }

    def get_queryset(self):
        queryset = super(PlaylistViewSet, self).get_queryset()
        queryset = self.filter_hidden(queryset)
        queryset = self.filter_ordering(queryset)
        return queryset


class RecommendedMoviesView(APIView):
    permission_classes = [IsAuthenticated]

    def get_limit(self):
        try:
            limit = int(
                self.request.query_params.get(
                    "limit",
                    settings.REST_FRAMEWORK["PAGE_SIZE"]
                )
            )
        except Exception:
            limit = settings.REST_FRAMEWORK["PAGE_SIZE"]
        return limit

    def get_hidden_filter(self, qs):
        hidden_param = self.request.query_params.get("hidden")
        if not self.request.user.is_superuser:
            return qs.filter(hidden=False)
        else:
            if hidden_param is not None:
                if hidden_param.lower() == "true":
                    return qs.filter(hidden=True)
                elif hidden_param.lower() == "false":
                    return qs.filter(hidden=False)
        return qs

    def get_similar_movies(self, movie_hash, limit):
        try:
            base_movie = Movie.objects.get(hash=movie_hash)
        except Movie.DoesNotExist:
            return Movie.objects.none()

        vector = (SearchVector("title", weight='A') +
                  SearchVector("subtitle", weight='B') +
                  SearchVector("description", weight='C'))
        query = SearchQuery(base_movie.title)
        qs = Movie.objects.annotate(
            rank=SearchRank(vector, query)
        ).filter(
            rank__gte=0.1
        ).exclude(id=base_movie.id)

        base_tags = base_movie.tag.all()
        base_genres = base_movie.genre.all()

        qs = qs.filter(Q(tag__in=base_tags) | Q(
            genre__in=base_genres)).distinct()

        qs = qs.annotate(
            common_tags=Count('tag', filter=Q(tag__in=base_tags)),
            common_genres=Count('genre', filter=Q(genre__in=base_genres))
        ).annotate(
            total_common=F('common_tags') + F('common_genres')
        )

        qs = self.get_hidden_filter(qs)

        qs = qs.order_by("-rank", "-total_common")[:limit]
        return qs

    def get_user_recommended_movies(self, user, limit):

        watched_ids = list(Progress.objects.filter(
            user=user,
            movie__isnull=False
        ).values_list("movie__id", flat=True))
        watchlist_ids = list(WatchList.objects.filter(
            user=user,
            movie__isnull=False
        ).values_list("movie__id", flat=True))
        user_movies_ids = set(watched_ids + watchlist_ids)
        if not user_movies_ids:
            qs = Movie.objects.all()
            qs = self.get_hidden_filter(qs)
            return qs.order_by("-created_date")[:limit]

        user_tags = Tag.objects.filter(
            movie__id__in=user_movies_ids).distinct()
        user_genres = Genre.objects.filter(
            movie__id__in=user_movies_ids).distinct()
        user_tag_ids = list(user_tags.values_list("id", flat=True))
        user_genre_ids = list(user_genres.values_list("id", flat=True))
        qs = Movie.objects.filter(
            Q(tag__in=user_tag_ids) | Q(genre__in=user_genre_ids)
        ).exclude(id__in=user_movies_ids).distinct()
        qs = self.get_hidden_filter(qs)

        qs = qs.annotate(
            match_count=Count("id")
        ).order_by("?")[:limit]

        return qs

    def get_collaborative_recommendations(self, user, limit):
        watched_ids = list(
            Progress.objects.filter(
                user=user,
                movie__isnull=False
            ).values_list("movie__id", flat=True)
        )
        watchlist_ids = list(
            WatchList.objects.filter(
                user=user,
                movie__isnull=False
            ).values_list("movie__id", flat=True)
        )
        current_movie_ids = set(watched_ids + watchlist_ids)

        similar_user_ids_progress = Progress.objects.filter(
            movie__id__in=current_movie_ids
        ).exclude(user=user).values_list("user_id", flat=True)
        similar_user_ids_watchlist = WatchList.objects.filter(
            movie__id__in=current_movie_ids
        ).exclude(user=user).values_list("user_id", flat=True)
        similar_user_ids = set(
            list(similar_user_ids_progress) + list(similar_user_ids_watchlist))
        if not similar_user_ids:
            return Movie.objects.none()

        qs = Movie.objects.filter(
            Q(progress__user__id__in=similar_user_ids) |
            Q(watchlist__user__id__in=similar_user_ids)
        ).exclude(id__in=current_movie_ids).distinct()

        qs = qs.annotate(
            similarity_score=Count(
                "progress",
                filter=Q(progress__user__id__in=similar_user_ids)
            ) + Count(
                "watchlist",
                filter=Q(watchlist__user__id__in=similar_user_ids)
            )
        )

        qs = self.get_hidden_filter(qs)
        qs = qs.order_by("-similarity_score")[:limit]
        return qs

    def get(self, request, format=None):
        user = request.user
        limit = self.get_limit()
        movie_hash = request.query_params.get("hash")

        if movie_hash:
            cf_list = list(self.get_similar_movies(movie_hash, limit))
            if len(cf_list) < limit:
                remaining = limit - len(cf_list)
                simple_list = list(
                    self.get_user_recommended_movies(user, limit * 2))
                cf_ids = set([movie.id for movie in cf_list])
                additional = [
                    movie for movie in simple_list if movie.id not in cf_ids]
                additional = additional[:remaining]
                qs = cf_list + additional
        else:
            cf_list = list(self.get_collaborative_recommendations(user, limit))
            if len(cf_list) < limit:
                remaining = limit - len(cf_list)
                simple_list = list(
                    self.get_user_recommended_movies(user, limit * 2))
                cf_ids = set([movie.id for movie in cf_list])
                additional = [
                    movie for movie in simple_list if movie.id not in cf_ids]
                additional = additional[:remaining]
                combined = cf_list + additional
            else:
                combined = cf_list
            qs = combined

        serializer = MovieSerializer(
            qs, many=True, context={"request": request})
        return Response(serializer.data)


class SubtitleView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, movie_hash, language):
        if language == "PT":
            language = "pt-br"

        if language == "EN":
            language = "pt-br"

        if language not in ["pt-br", "en-us"]:
            return Response({
                "error": "Invalid Language. Supported: [PT, EN]"
            }, status=400)

        movie = Movie.objects.filter(hash=movie_hash).first()
        if not movie:
            return Response({
                "error": "Movie not found"
            }, status=400)

        if language == "pt-br":
            if movie.subtitle and movie.subtitle.language in ["PT", "pt"]:
                return Response({
                    "error": "Movie already has a Portuguese subtitle"
                }, status=400)

        if language == "en-us":
            if movie.subtitle and movie.subtitle.language in ["EN", "en"]:
                return Response({
                    "error": "Movie already has a English subtitle"
                }, status=400)

        file_id = helper.get_subtitle(movie, language)

        if not file_id:
            return Response({
                "error": "No matching subtitle found"
            }, status=400)

        url = helper.download_subtitle(file_id)

        if not url:
            return Response({
                "error": "Failed to download subtitle"
            }, status=400)

        vtt = helper.parse_subtitle(url)

        if not vtt:
            return Response({
                "error": "Failed to process subtitle file"
            }, status=400)

        subtitle = Subtitle(language="PT", label="Portuguese", vtt=vtt)
        subtitle.save()

        movie.subtitle = subtitle
        movie.save()

        return Response({
            "movie": movie.title,
            "language": language,
            "subtitle": vtt
        }, status=200)

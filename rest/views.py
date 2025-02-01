from content.models import Content
from content.models import Episode
from content.models import Genre
from content.models import Media
from content.models import Movie
from content.models import Season
from content.models import Tag
from django_filters.rest_framework import DjangoFilterBackend
from rest.middlewares import IsSuperUserOrVisibleOnly
from rest.mixins import HiddenFilterMixin
from rest.mixins import OrderingMixin
from rest.pagination import CustomPageNumberPagination
from rest.serializers import ContentSerializer
from rest.serializers import EpisodeSerializer
from rest.serializers import GenreSerializer
from rest.serializers import MediaSerializer
from rest.serializers import MovieSerializer
from rest.serializers import SeasonSerializer
from rest.serializers import TagSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class GenericViewSet(HiddenFilterMixin,
                     OrderingMixin,
                     viewsets.ModelViewSet):
    pass


class GenreViewSet(GenericViewSet):
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


class GenreMoviesViewSet(GenericViewSet):
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


class TagViewSet(GenericViewSet):
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


class TagMoviesViewSet(GenericViewSet):
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


class MovieViewSet(GenericViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticated, IsSuperUserOrVisibleOnly]
    filter_backends = [DjangoFilterBackend]
    pagination_class = CustomPageNumberPagination

    allowed_order_fields = {
        "date": "date",
        "title": "title"
    }

    def get_queryset(self):
        queryset = super(MovieViewSet, self).get_queryset()
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


class ContentViewSet(GenericViewSet):
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


class ContentMediasViewSet(GenericViewSet):
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


class MediaSeasonsViewSet(GenericViewSet):
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


class SeasonEpisodesViewSet(GenericViewSet):
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

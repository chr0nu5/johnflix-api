from content.models import Genre
from content.models import Movie
from content.models import Tag
from django_filters.rest_framework import DjangoFilterBackend
from rest.middlewares import IsSuperUserOrVisibleOnly
from rest.pagination import CustomPageNumberPagination
from rest.serializers import GenreSerializer
from rest.serializers import MovieSerializer
from rest.serializers import TagSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAuthenticated, IsSuperUserOrVisibleOnly]
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        user = self.request.user
        queryset = Genre.objects.all()

        if not user.is_superuser:
            return queryset.filter(hidden=False)

        hidden_param = self.request.query_params.get("hidden")
        if hidden_param is not None:
            if hidden_param.lower() == "true":
                return queryset.filter(hidden=True)
            elif hidden_param.lower() == "false":
                return queryset.filter(hidden=False)

        return queryset


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated, IsSuperUserOrVisibleOnly]
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        user = self.request.user
        queryset = Tag.objects.all()

        if not user.is_superuser:
            return queryset.filter(hidden=False)

        hidden_param = self.request.query_params.get("hidden")
        if hidden_param is not None:
            if hidden_param.lower() == "true":
                return queryset.filter(hidden=True)
            elif hidden_param.lower() == "false":
                return queryset.filter(hidden=False)

        return queryset


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticated, IsSuperUserOrVisibleOnly]
    filter_backends = [DjangoFilterBackend]
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        user = self.request.user
        queryset = Movie.objects.all()

        if not user.is_superuser:
            queryset = queryset.filter(hidden=False)
        else:
            hidden_param = self.request.query_params.get("hidden")
            if hidden_param is not None:
                if hidden_param.lower() == "true":
                    queryset = queryset.filter(hidden=True)
                elif hidden_param.lower() == "false":
                    queryset = queryset.filter(hidden=False)

        genre_ids = self.request.query_params.get("genre")
        if genre_ids:
            genre_ids = genre_ids.split(",")
            queryset = queryset.filter(genre__id__in=genre_ids).distinct()

        tag_ids = self.request.query_params.get("tag")
        if tag_ids:
            tag_ids = tag_ids.split(",")
            queryset = queryset.filter(tag__id__in=tag_ids).distinct()

        order_by = self.request.query_params.get("order_by")
        order_direction = self.request.query_params.get(
            "order_direction",
            "asc"
        ).lower()

        valid_order_fields = {"date": "date", "title": "title"}
        if order_by in valid_order_fields:
            ordering_field = valid_order_fields[order_by]
            if order_direction == "desc":
                ordering_field = f"-{ordering_field}"
            queryset = queryset.order_by(ordering_field)

        return queryset

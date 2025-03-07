import os

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
from django.db.models import F
from rest.fields import CDNFileField
from rest_framework import serializers


class BaseCDNModelSerializer(serializers.ModelSerializer):
    def get_fields(self):
        fields = super().get_fields()
        for field_name, field in fields.items():
            if isinstance(field, serializers.FileField):
                fields[field_name] = CDNFileField()
        return fields


class GenreSerializer(BaseCDNModelSerializer):
    cover = CDNFileField()

    class Meta:
        model = Genre
        fields = ('hash', 'name', 'cover')


class TagSerializer(BaseCDNModelSerializer):
    cover = CDNFileField()

    class Meta:
        model = Tag
        fields = ('hash', 'name', 'cover')


class SubtitleSerializer(BaseCDNModelSerializer):
    vtt = CDNFileField()

    class Meta:
        model = Subtitle
        fields = ('language', 'label', 'vtt')


class MovieSerializer(BaseCDNModelSerializer):
    tag = TagSerializer(many=True, read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    progress = serializers.SerializerMethodField()
    subtitle = SubtitleSerializer(read_only=True)
    watchlist = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    next = serializers.SerializerMethodField()

    def get_next(self, obj):

        if self.context.get('is_next'):
            return None

        playlist = Playlist.objects.filter(movies=obj).first()
        if playlist:
            next_movie = playlist.movies.filter(
                date__gt=obj.date if obj.date else obj.created_date
            ).order_by('date').first()
            if next_movie:
                context = self.context.copy()
                context["next="] = True
                return MovieSerializer(next_movie, context=context).data

        return None

    def get_type(self, obj):
        return "movie"

    def get_progress(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            progress_obj = Progress.objects.filter(
                movie=obj,
                user=request.user
            ).first()
            if progress_obj and progress_obj.time is not None:
                return progress_obj.time
        return 0

    def get_watchlist(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return obj.is_watchlist(request.user, WatchList)
        return False

    class Meta:
        model = Movie
        # fields = '__all__'
        exclude = ['created_date', 'modified_date',
                   'hidden', 'id', 'bypass_metadata', 'metadata']


class ContentSerializer(BaseCDNModelSerializer):
    class Meta:
        model = Content
        fields = '__all__'


class MediaSerializer(BaseCDNModelSerializer):
    class Meta:
        model = Media
        fields = '__all__'


class SeasonSerializer(BaseCDNModelSerializer):
    class Meta:
        model = Season
        fields = '__all__'


class EpisodeSerializer(BaseCDNModelSerializer):
    tag = TagSerializer(many=True, read_only=True)
    season = serializers.SerializerMethodField()
    number = serializers.SerializerMethodField()
    progress = serializers.SerializerMethodField()
    genre = serializers.SerializerMethodField()
    show = serializers.SerializerMethodField()
    watchlist = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    next = serializers.SerializerMethodField()

    def get_type(self, obj):
        return "episode"

    def get_genre(self, obj):
        return []

    def get_show(self, obj):
        return obj.season.media.name

    def get_season(self, obj):
        if obj.season and obj.season.number is not None:
            return "{:02d}".format(obj.season.number)
        return None

    def get_number(self, obj):
        if obj.number is not None:
            return "{:02d}".format(obj.number)
        return None

    def get_progress(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            progress_obj = Progress.objects.filter(
                episode=obj,
                user=request.user
            ).first()
            if progress_obj and progress_obj.time is not None:
                return progress_obj.time
        return 0

    def get_watchlist(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return obj.is_watchlist(request.user, WatchList)
        return False

    def get_next(self, obj):

        if self.context.get('is_next'):
            return None

        next_episode = Episode.objects.filter(
            season=obj.season,
            number=obj.number + 1
        ).first()

        if next_episode:
            return EpisodeSerializer(
                next_episode,
                context={**self.context, 'is_next': True}).data

        next_season = Season.objects.filter(
            media=obj.season.media,
            number=obj.season.number + 1
        ).first()

        if next_season:
            first_episode_next_season = Episode.objects.filter(
                season=next_season,
                number=1
            ).first()

            if first_episode_next_season:
                return EpisodeSerializer(
                    first_episode_next_season,
                    context={**self.context, 'is_next': True}).data

        return None

    class Meta:
        model = Episode
        exclude = ['created_date', 'modified_date', 'hidden', 'id']


class PhotoCollectionSerializer(BaseCDNModelSerializer):

    class Meta:
        model = PhotoCollection
        exclude = ['photos', 'id', 'hidden',
                   'created_date', 'modified_date', 'tag', 'genre']


class PhotoSerializer(BaseCDNModelSerializer):

    class Meta:
        model = Photo
        exclude = ['id', 'hidden', 'created_date', 'modified_date']


class PlaylistSerializer(BaseCDNModelSerializer):
    movies = MovieSerializer(many=True, read_only=True)

    class Meta:
        model = Playlist
        exclude = ['id', 'hidden', 'created_date', 'modified_date']

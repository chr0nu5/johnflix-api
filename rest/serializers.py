import os

from content.models import Content
from content.models import Episode
from content.models import Genre
from content.models import Media
from content.models import Movie
from content.models import Season
from content.models import Tag
from content.models import WatchList
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


class MovieSerializer(BaseCDNModelSerializer):
    tag = TagSerializer(many=True, read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    watchlist = serializers.SerializerMethodField()

    def get_watchlist(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return obj.is_watchlist(request.user, WatchList)
        return False

    class Meta:
        model = Movie
        # fields = '__all__'
        exclude = ['created_date', 'modified_date',
                   'hidden', 'id', 'bypass_metadata', 'metadata', 'embed']


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
    watchlist = serializers.SerializerMethodField()

    def get_season(self, obj):
        if obj.season and obj.season.number is not None:
            return "{:02d}".format(obj.season.number)
        return None

    def get_number(self, obj):
        if obj.number is not None:
            return "{:02d}".format(obj.number)
        return None

    def get_watchlist(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return obj.is_watchlist(request.user, WatchList)
        return False

    class Meta:
        model = Episode
        # fields = '__all__'
        exclude = ['created_date', 'modified_date', 'hidden', 'id']

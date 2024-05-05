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
from content.models import WatchParty
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.models import Group


class ContentAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_cover', 'created_date', 'hidden', 'link']
    list_filter = ['created_date', 'hidden']
    list_editable = ['hidden']
    exclude = ['hash']


class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_cover', 'cover', 'created_date', 'hidden',
                    'link', 'featured', 'order']
    list_filter = ['created_date', 'hidden']
    list_editable = ['hidden', 'featured', 'order', 'cover']
    exclude = ['hash']


class MediaAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_cover', 'date',
                    'created_date', 'hidden', 'link']
    list_filter = ['date', 'created_date', 'hidden']
    list_editable = ['date', 'hidden']
    filter_horizontal = ['genre']
    exclude = ['hash']


class SeasonAdmin(admin.ModelAdmin):
    list_display = ['media', 'title', 'number', 'date',
                    'created_date', 'hidden', 'link']
    list_filter = ['date', 'created_date', 'hidden']
    list_editable = ['title', 'date', 'hidden']
    exclude = ['hash']


class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_cover', 'created_date', 'cover',
                    'hidden', 'link', 'order']
    list_filter = ['created_date', 'hidden']
    list_editable = ['hidden', 'cover', 'order']
    search_fields = ['name']
    exclude = ['hash']


class SubtitleAdmin(admin.ModelAdmin):
    list_display = ['language', 'label', 'vtt']


class EpisodeAdmin(admin.ModelAdmin):
    list_display = ['title', 'season', 'number',
                    'get_cover', 'media', 'duration', 'date',
                    'hidden', 'link']
    list_filter = ['date', 'created_date', 'hidden']
    list_editable = ['date', 'hidden']
    filter_horizontal = ['tag']
    search_fields = ['title']
    exclude = ['hash']


class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'get_cover', 'cover',
                    'duration', 'date', 'hidden', 'link']
    list_filter = ['date', 'created_date', 'hidden', 'tag', 'genre']
    list_editable = ['date', 'cover', 'hidden']
    filter_horizontal = ['tag', 'genre']
    search_fields = ['title']
    exclude = ['hash', 'metadata', 'bypass_metadata']


class ProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'episode', 'movie', 'time', 'speed']


class PhotoAdmin(admin.ModelAdmin):
    list_display = ['id', 'photo', 'hidden', 'created_date']
    list_editable = ['hidden']
    exclude = ['hash']


class PhotoCollectionAdmin(admin.ModelAdmin):
    list_display = ['hash', 'title', 'cover', 'hidden', 'link']
    filter_horizontal = ['tag', 'genre', 'photos']
    list_editable = ['hidden']
    search_fields = ['title']
    exclude = ['hash']


class WatchListAdmin(admin.ModelAdmin):
    list_display = ['user', 'episode', 'movie']


class WatchPartyAdmin(admin.ModelAdmin):
    list_display = ['hash', 'user', 'movie', 'playing', 'current_time', 'link']


class PlaylistAdmin(admin.ModelAdmin):
    list_display = ['pk', 'get_cover', 'name', 'link', 'hidden']
    list_editable = ['name', 'hidden']
    exclude = ['hash']


admin.site.register(Content, ContentAdmin)
admin.site.register(Episode, EpisodeAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Media, MediaAdmin)
admin.site.register(Movie, MovieAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(PhotoCollection, PhotoCollectionAdmin)
admin.site.register(Progress, ProgressAdmin)
admin.site.register(Season, SeasonAdmin)
admin.site.register(Subtitle, SubtitleAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(WatchList, WatchListAdmin)
admin.site.register(WatchParty, WatchPartyAdmin)
admin.site.register(Playlist, PlaylistAdmin)

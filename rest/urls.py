from django.urls import include
from django.urls import path
from rest.views import AddOrRemoveWatchListView
from rest.views import ContentMediasViewSet
from rest.views import ContentViewSet
from rest.views import EpisodeViewSet
from rest.views import GalleriesViewSet
from rest.views import GalleryPhotosViewSet
from rest.views import GenreMoviesViewSet
from rest.views import GenreViewSet
from rest.views import MediaSeasonsViewSet
from rest.views import MovieViewSet
from rest.views import PlaylistViewSet
from rest.views import ProgressSaveView
from rest.views import RecommendedMoviesView
from rest.views import SearchView
from rest.views import SeasonEpisodesViewSet
from rest.views import SubtitleView
from rest.views import TagMoviesViewSet
from rest.views import TagViewSet
from rest.views import UserProfileView
from rest.views import UserWatchingView
from rest.views import UserWatchlistView
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register(r'tags', TagViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'movies', MovieViewSet)
router.register(r'episode', EpisodeViewSet)
router.register(r'contents', ContentViewSet)
router.register(r'playlists', PlaylistViewSet)

urlpatterns = [
    path(
        'content/<str:hash>/medias/',
        ContentMediasViewSet.as_view({'get': 'list'}),
        name='content-medias'
    ),
    path(
        'media/<str:hash>/seasons/',
        MediaSeasonsViewSet.as_view({'get': 'list'}),
        name='media-seasons'
    ),
    path(
        'season/<str:hash>/episodes/',
        SeasonEpisodesViewSet.as_view({'get': 'list'}),
        name='season-episodes'
    ),
    path(
        'genre/<str:hash>/movies/',
        GenreMoviesViewSet.as_view({'get': 'list'}),
        name='genre-movies'
    ),
    path(
        'tag/<str:hash>/movies/',
        TagMoviesViewSet.as_view({'get': 'list'}),
        name='tag-movies'
    ),

    path(
        'galleries/',
        GalleriesViewSet.as_view({"get": "list"}),
        name='galleries'
    ),
    path(
        'gallery/<str:hash>/photos/',
        GalleryPhotosViewSet.as_view({"get": "list"}),
        name='gallery-photos'
    ),

    path(
        'user/profile/',
        UserProfileView.as_view(),
        name='user-profile'
    ),
    path(
        'user/watchlist/',
        UserWatchlistView.as_view(),
        name='user-watchlist'
    ),
    path(
        'user/watchlist/save/',
        AddOrRemoveWatchListView.as_view(),
        name='user-watchlist-update'
    ),
    path(
        'user/progress/',
        ProgressSaveView.as_view(),
        name='user-progress-save'
    ),
    path(
        'user/watching/',
        UserWatchingView.as_view(),
        name='user-watching'
    ),

    path(
        'search/',
        SearchView.as_view(),
        name='search'
    ),

    path(
        "recommended/",
        RecommendedMoviesView.as_view(),
        name="recommended-movies"
    ),

    path(
        'subtitle/<str:movie_hash>/<str:language>/',
        SubtitleView.as_view(),
        name='subtitle-fetch'
    ),

    path('', include(router.urls)),
]

urlpatterns += [
    path(
        'auth/login/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'auth/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),
]

from django.urls import include
from django.urls import path
from rest.views import ContentMediasViewSet
from rest.views import ContentViewSet
from rest.views import GenreMoviesViewSet
from rest.views import GenreViewSet
from rest.views import MediaSeasonsViewSet
from rest.views import MovieViewSet
from rest.views import SeasonEpisodesViewSet
from rest.views import TagMoviesViewSet
from rest.views import TagViewSet
from rest.views import UserWatchlistView
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register(r'tags', TagViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'movies', MovieViewSet)
router.register(r'contents', ContentViewSet)

urlpatterns = [
    path(
        'v2/content/<str:hash>/medias/',
        ContentMediasViewSet.as_view({'get': 'list'}),
        name='content-medias'
    ),
    path(
        'v2/media/<str:hash>/seasons/',
        MediaSeasonsViewSet.as_view({'get': 'list'}),
        name='media-seasons'
    ),
    path(
        'v2/season/<str:hash>/episodes/',
        SeasonEpisodesViewSet.as_view({'get': 'list'}),
        name='season-episodes'
    ),
    path(
        'v2/genre/<str:hash>/movies/',
        GenreMoviesViewSet.as_view({'get': 'list'}),
        name='genre-movies'
    ),
    path(
        'v2/tag/<str:hash>/movies/',
        TagMoviesViewSet.as_view({'get': 'list'}),
        name='tag-movies'
    ),

    path(
        'v2/user/watchlist/',
        UserWatchlistView.as_view(),
        name='user-watchlist'
    ),

    path('v2/', include(router.urls)),
]

urlpatterns += [
    path(
        'v2/auth/login/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'v2/auth/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),
]

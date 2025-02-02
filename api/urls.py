from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from api.views import BlankView

from content.views import AllMoviesView
from content.views import AuthView
from content.views import ContentView
from content.views import EpisodeView
from content.views import GenreView
from content.views import LatestView
from content.views import MediaView
from content.views import MovieView
from content.views import PhotoView
from content.views import PlaylistView
from content.views import ProgressView
from content.views import RandomView
from content.views import RecommendedView
from content.views import SearchView
from content.views import SeasonView
from content.views import SubtitleView
from content.views import TagView
from content.views import UserView
from content.views import WatchPartyView
from content.views import WathListView

urlpatterns = [

    # admin
    path('admin/', admin.site.urls),

    path('', include('rest.urls')),

    # API
    # user
    path('user', UserView.as_view()),
    path('user/login', AuthView.as_view()),

    path('progress', ProgressView.as_view()),
    path('progress/<slug:hash>', ProgressView.as_view()),

    path('content', ContentView.as_view()),
    path('content/<slug:hash>', ContentView.as_view()),

    path('media/<slug:hash>', MediaView.as_view()),

    path('season/<slug:hash>', SeasonView.as_view()),

    path('genre', GenreView.as_view()),
    path('genre/<slug:hash>', GenreView.as_view()),

    path('tag', TagView.as_view()),
    path('tag/<slug:hash>', TagView.as_view()),

    path('episode/<slug:hash>', EpisodeView.as_view()),
    path('movie/<slug:hash>', MovieView.as_view()),

    path('movies/all', AllMoviesView.as_view()),
    path('subtitle/<slug:hash>/<slug:language>', SubtitleView.as_view()),

    path('photo', PhotoView.as_view()),
    path('photo/<slug:hash>', PhotoView.as_view()),

    path('latest/<slug:type>', LatestView.as_view()),

    path('random/<slug:type>', RandomView.as_view()),

    path('search', SearchView.as_view()),

    path('recommended', RecommendedView.as_view()),

    path('watchlist', WathListView.as_view()),

    path('watchparty', WatchPartyView.as_view()),
    path('watchparty/<slug:hash>', WatchPartyView.as_view()),
    path('watchparty/<slug:hash>/<slug:id>', WatchPartyView.as_view()),

    path('playlist', PlaylistView.as_view()),
    path('playlist/<slug:hash>', PlaylistView.as_view()),

    # # home
    path('', BlankView.as_view()),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

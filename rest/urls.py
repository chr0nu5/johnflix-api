from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest.views import MovieViewSet, GenreViewSet, TagViewSet
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register(r'tags', TagViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'movies', MovieViewSet)

urlpatterns = [
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

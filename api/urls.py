from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from api.views import BlankView

urlpatterns = [

    # admin
    path('admin/', admin.site.urls),

    # default
    path('', BlankView.as_view()),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

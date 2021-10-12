from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static
from django.conf import settings

app_name = 'rootProject'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tweetApp.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


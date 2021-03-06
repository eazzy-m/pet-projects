from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('catalog.urls')),
    path('news/', include('news.urls')),
    path('weather/', include('weather.urls')),
    path('forum/', include('forum.urls')),
    path('captcha/', include('captcha.urls'))

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

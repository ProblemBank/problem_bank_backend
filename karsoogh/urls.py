from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from karsoogh import settings

urlpatterns = \
    [
        path('admin/', admin.site.urls),
        path('api/account/', include('Account.urls')),
        path('api/game/', include('Game.urls')),
        path('api/auction/', include('auction.urls')),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

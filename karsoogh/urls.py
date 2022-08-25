from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from django.conf import settings

urlpatterns = \
    [
        path('api/admin/', admin.site.urls),
        path('api/account/', include('Account.urls')),
        # path('api/game/', include('Game.urls')),
        path('api/game2/', include('Game2.urls')),
        path('api/problembank/', include('problembank.urls')),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

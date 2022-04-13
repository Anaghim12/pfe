
from django.contrib import admin
from django.urls import path , include

admin.site.site_header ='Storefront Admin'
admin.site.index_title ='Admin'
#test image
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('playground/', include('playground.urls')),
    path('store/', include('store.urls')),
    path('utilisateur/', include('core.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('__debug__/', include('debug_toolbar.urls')),
    #to connect with FB+Gmail
    path('auth/', include('djoser.social.urls')),
]
# pour tester les images
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
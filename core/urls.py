from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # allauth urls
    path('accounts/', include('allauth.urls')),

    # my apps urls
    path('', include('jobs.urls')),
    path('', include('profiles.urls')),
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('products.urls')),
]

urlpatterns += [
    path(
        'media/<path:path>',
        serve,
        {
            'document_root': settings.MEDIA_ROOT,
        },
    ),
]

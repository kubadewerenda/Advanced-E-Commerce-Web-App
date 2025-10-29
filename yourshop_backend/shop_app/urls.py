from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.http import JsonResponse
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/', include('apps.users.urls')),
    path('api/', include('apps.shipping.urls')),
    path('api/', include('apps.categories.urls')),
    path('api/', include('apps.products.urls')),
    path('api/', include('apps.cart.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

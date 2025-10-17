"""
URL configuration for SmartSales365 project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # API Endpoints
    path('api/auth/', include('apps.users.urls')),
    path('api/products/', include('apps.products.urls')),
    path('api/stores/', include('apps.stores.urls')),
    path('api/orders/', include('apps.orders.urls')),
    path('api/ratings/', include('apps.ratings.urls')),
    path('api/coupons/', include('apps.coupons.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

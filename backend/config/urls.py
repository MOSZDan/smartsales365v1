"""
URL configuration for SmartSales365 project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


def api_root(request):
    """Root endpoint with API information"""
    return JsonResponse({
        'message': 'SmartSales365 API',
        'version': '1.0.0',
        'status': 'running',
        'endpoints': {
            'documentation': '/api/docs/',
            'schema': '/api/schema/',
            'admin': '/admin/',
            'auth': '/api/auth/',
            'products': '/api/products/',
            'stores': '/api/stores/',
            'orders': '/api/orders/',
            'ratings': '/api/ratings/',
            'coupons': '/api/coupons/',
        }
    })

urlpatterns = [
    # Root
    path('', api_root, name='api-root'),

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



from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from apps.customers import api as customers_api

schema_view = get_schema_view(
    openapi.Info(
        title="Savannah Informatics API",
        default_version='v1',
        description="E-commerce service API documentation",
        terms_of_service="https://www.savannahinformatics.com/terms/",
        contact=openapi.Contact(email="info@savannahinformatics.com"),
        license=openapi.License(name="Proprietary License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.products.api.urls')),
    path('api/', include('apps.orders.api.urls')),
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # CHANGE THESE URL PATTERNS to avoid conflict
    path('api/customer/check/', customers_api.check_customer, name='check-customer'),
    path('api/customer/orders/', customers_api.customer_orders, name='customer-orders'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
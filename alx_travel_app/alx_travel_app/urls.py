from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from listings.views import InitiatePaymentView, VerifyPaymentView
schema_view = get_schema_view(
   openapi.Info(
      title="Travel App API",
      default_version='v1',
      description="API documentation for Listings and Bookings",
      terms_of_service="https://www.yourapp.com/terms/",
        contact=openapi.Contact(email="contact@yourapp.com"),
        license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('listings.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
     path('api/payments/initiate/', InitiatePaymentView.as_view(), name='initiate-payment'),
    path('api/payments/verify/', VerifyPaymentView.as_view(), name='verify-payment'),
]
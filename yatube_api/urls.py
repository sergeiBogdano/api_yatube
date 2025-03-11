from django.urls import include, path
from rest_framework.routers import DefaultRouter


urlpatterns = [
    path('api/v1/', include('api.urls')),
]

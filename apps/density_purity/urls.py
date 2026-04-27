from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DensityPurityViewSet

router = DefaultRouter()
router.register(r'', DensityPurityViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

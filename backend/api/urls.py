from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DatasetViewSet, UploadViewSet

router = DefaultRouter()
router.register(r'datasets', DatasetViewSet, basename='dataset')
router.register(r'upload', UploadViewSet, basename='upload')

urlpatterns = [
    path('', include(router.urls)),
]

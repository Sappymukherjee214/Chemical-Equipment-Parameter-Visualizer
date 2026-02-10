from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DatasetViewSet, UploadViewSet, create_superuser

router = DefaultRouter()
router.register(r'datasets', DatasetViewSet, basename='dataset')
router.register(r'upload', UploadViewSet, basename='upload')

urlpatterns = [
    path('', include(router.urls)),
    path('create-superuser/', create_superuser, name='create-superuser'),
]

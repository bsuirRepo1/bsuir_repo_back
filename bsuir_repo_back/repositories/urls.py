from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views.repository import RepositoryViewSet

router = DefaultRouter()
router.register(r'repositories', RepositoryViewSet, basename='repositories')

urlpatterns = [
] + router.urls

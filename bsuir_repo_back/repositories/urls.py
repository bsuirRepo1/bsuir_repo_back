from rest_framework.routers import DefaultRouter
from django.urls import path

from .views import RepositoryViewSet, FilterRepoView

router = DefaultRouter()
router.register(r'repositories', RepositoryViewSet, basename='repositories')

urlpatterns = [
    path('users/', FilterRepoView.as_view(), name='filter'),
] + router.urls

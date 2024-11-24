from rest_framework.routers import DefaultRouter

from .views.repositories import RepositoryViewSet

router = DefaultRouter()
router.register(r'repositories', RepositoryViewSet, basename='repositories')

urlpatterns = [
] + router.urls

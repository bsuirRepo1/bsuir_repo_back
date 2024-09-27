from django.urls import path
from rest_framework import routers

from .views import RegisterView, LoginView, UserViewSet, UserByNameView

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('users/<str:username>/', UserByNameView.as_view(), name='user_by_name'),
] + router.urls

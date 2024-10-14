from django.urls import path
from rest_framework import routers

from .views import (RegisterView, LoginView, UserViewSet, UserByNameView, ChangePasswordView, ChangePasswordConfirmView,
                    LogoutView, ProfileViewSet, ConfirmRegisterView, ForgotPasswordView)

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'profile', ProfileViewSet, basename='profile')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('users/<str:username>/', UserByNameView.as_view(), name='user_by_name'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('change-password-confirm/', ChangePasswordConfirmView.as_view(), name='change_password_confirm'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('confirm-register/', ConfirmRegisterView.as_view(), name='confirm-register'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
] + router.urls

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import LoginWithOTP, ValidateOTP, LogoutView, UserViewSet


router = DefaultRouter()

router.register('user', UserViewSet, basename='user')

urlpatterns = [
    path('login/', LoginWithOTP.as_view(), name='login'),
    path('validate-otp/', ValidateOTP.as_view(), name='validate-otp'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', include(router.urls))
]

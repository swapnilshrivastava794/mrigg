from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterView, CustomTokenObtainPairView, ProfileView,UpdateProfileView,RequestOTPView,VerifyOTPChangePasswordView,LogoutView,ResendOTPView

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='api_register'),
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='api_login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='api_refresh'),
    path('auth/me/', ProfileView.as_view(), name='api_me'),
    path('auth/update-profile/' , UpdateProfileView.as_view()),
    path('auth/request-otp/', RequestOTPView.as_view()),
    path('auth/verify-otp-change-password/', VerifyOTPChangePasswordView.as_view()),
    path('auth/resend-otp/', ResendOTPView.as_view()),
    path('auth/logout/', LogoutView.as_view()),
]

from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)


urlpatterns = [
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('googlelogin/', GoogleLoginView.as_view()),
    path('otp/', OtpView.as_view()),
    path('profile/<uuid:id>', UserDetailsView.as_view()),
    path('instructorprofile/<uuid:id>', InstructorProfileView.as_view())
    
]

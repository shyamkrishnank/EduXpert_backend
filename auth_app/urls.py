from django.urls import path
from .views import *


urlpatterns = [
  
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('googlelogin/', GoogleLoginView.as_view()),
    path('otp/', OtpView.as_view()),
    path('profile/<int:id>', UserDetailsView.as_view()),
    path('instructorprofile/<int:id>', InstructorProfileView.as_view())
    
]

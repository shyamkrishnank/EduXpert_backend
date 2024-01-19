from django.urls import path
from .views import *



urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('googlelogin/', GoogleLoginView.as_view()),
    path('googlesignup/', GoogleSignUpView.as_view()),
    path('resend_otp/',ResendOTP.as_view()),
    path('is_staff/<str:is_staff>/<uuid:user_id>', GoogleSignUpView.as_view()),
    path('otp/', OtpView.as_view()),
    path('profile/<uuid:id>', UserDetailsView.as_view()),
    path('instructorprofile/<uuid:id>', InstructorProfileView.as_view()),
    path('forget_password/', ForgetPasswordView.as_view()),
    path('set_password/', NewPasswordView.as_view())
    
]

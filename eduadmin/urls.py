from django.urls import path
from .views import  *

urlpatterns = [
    path('login', AdminLogin.as_view()),
    path('course', CourseView.as_view()),
    path('course_details/<uuid:id>', CourseDetailedView.as_view()),
    path('course_status/<uuid:id>', CourseActivation.as_view()),
    path('users', UsersView.as_view()),
    path('users_details/<uuid:id>', UserDetailView.as_view()),
    path('user_status/<uuid:id>', UserActivation.as_view()),
    path('instructors', InstructorsView.as_view()),
    path('instructors_details/<uuid:id>', UserDetailView.as_view()),
    path('instructor_status/<uuid:id>', UserActivation.as_view()),

]
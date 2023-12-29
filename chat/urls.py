from django.urls import path
from .views import *

urlpatterns = [
    path('<uuid:id>', Chats.as_view()),
    path('data/<uuid:id>', ChatLists.as_view()),
]
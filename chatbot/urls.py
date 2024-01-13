from django.urls import path
from .views import *


urlpatterns = [
    path("",Chatbot.as_view())
]
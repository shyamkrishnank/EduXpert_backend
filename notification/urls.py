from django.urls import path
from .views import *

urlpatterns = [
    path('',Notifications.as_view() ),
    path('status/<uuid:id>', NotificationStatusChange.as_view())
]
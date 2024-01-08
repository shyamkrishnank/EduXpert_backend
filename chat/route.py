from django.urls import path
from .consumers import ChatConsumer
from notification.consumers import NotificationConsumer

websocket_urlpatterns = [
    path('ws/chat/', ChatConsumer.as_asgi()),
    path('ws/notification/', NotificationConsumer.as_asgi())
]
"""
ASGI config for backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from channels.routing import ProtocolTypeRouter, URLRouter
from chat.channelMiddleware import JWTwebsocketMiddleware

from django.core.asgi import get_asgi_application
from chat.route import websocket_urlpatterns
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    'http':django_asgi_app,
    'websocket':JWTwebsocketMiddleware(URLRouter(websocket_urlpatterns))
})

